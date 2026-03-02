import 'dart:async';

import 'package:flet/flet.dart';
import 'package:flutter/material.dart';
import 'package:sleek_circular_slider/sleek_circular_slider.dart';

String _canonicalKey(double val) {
  if (val == val.roundToDouble() && val.abs() < 1e15) {
    return val.toInt().toString();
  }
  return val.toStringAsFixed(10)
      .replaceAll(RegExp(r'0+$'), '')
      .replaceAll(RegExp(r'\.$'), '');
}

class FletCircularSliderControl extends StatefulWidget {
  final Control control;

  const FletCircularSliderControl({
    super.key,
    required this.control,
  });

  @override
  State<FletCircularSliderControl> createState() => _FletCircularSliderControlState();
}

class _FletCircularSliderControlState extends State<FletCircularSliderControl> {
  Timer? _throttleTimer;
  String? _lastFiredKey;
  String? _pendingKey;
  double? _pendingValue;

  void _fireChange(double value, String key) {
    if (key == _lastFiredKey) return;
    _lastFiredKey = key;
    widget.control.triggerEvent("change", value.toString());
  }

  void _flushPending() {
    if (!mounted) return;
    if (_pendingValue != null && _pendingKey != null) {
      _fireChange(_pendingValue!, _pendingKey!);
      _pendingValue = null;
      _pendingKey = null;
    }
  }

  void _onChangeThrottled(double snapped, String key, int throttleMs) {
    if (_throttleTimer == null || !_throttleTimer!.isActive) {
      _fireChange(snapped, key);
      _pendingValue = null;
      _pendingKey = null;
      _throttleTimer = Timer(Duration(milliseconds: throttleMs), _flushPending);
    } else {
      _pendingValue = snapped;
      _pendingKey = key;
    }
  }

  @override
  void dispose() {
    _throttleTimer?.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    double min = widget.control.getDouble("min", 0)!;
    double max = widget.control.getDouble("max", 100)!;
    double initialValue = widget.control.getDouble("value", 50)!;
    double sliderSize = widget.control.getDouble("size", 150)!;
    double startAngle = widget.control.getDouble("start_angle", 150)!;
    double angleRange = widget.control.getDouble("angle_range", 240)!;
    bool counterClockwise = widget.control.getBool("counter_clockwise", false)!;
    bool animationEnabled = widget.control.getBool("animation_enabled", true)!;

    // Label map (pre-computed by Python label_formatter, sent as native msgpack map)
    Map? labelMapRaw = widget.control.get("label_map");
    Map<String, String>? labelMap;
    if (labelMapRaw != null) {
      labelMap = labelMapRaw.map((k, v) => MapEntry(k.toString(), v.toString()));
    }

    // Track and bar widths
    double progressBarWidth = widget.control.getDouble("progress_bar_width", sliderSize / 10)!;
    double trackWidth = widget.control.getDouble("track_width", progressBarWidth / 4)!;
    double handlerSize = widget.control.getDouble("handler_size", progressBarWidth / 5)!;

    // Colors
    Color trackColor = widget.control.getColor("track_color", context) ?? const Color(0xFFDCBEFB);
    Color dotColor = widget.control.getColor("dot_color", context) ?? Colors.white;
    Color shadowColor = widget.control.getColor("shadow_color", context) ?? const Color(0xFF2C57C0);
    bool hideShadow = widget.control.getBool("hide_shadow", false)!;

    // Gradient colors for progress bar
    List<Color> progressBarColors;
    Color? sc = widget.control.getColor("progress_bar_start_color", context);
    Color? ec = widget.control.getColor("progress_bar_end_color", context);
    if (sc != null && ec != null) {
      progressBarColors = [sc, ec];
    } else {
      progressBarColors = [const Color(0xFF1E003B), const Color(0xFFEC008A), const Color(0xFF6285DA)];
    }

    // Info properties
    String? topLabel = widget.control.getString("top_label");
    String? bottomLabel = widget.control.getString("bottom_label");

    // Hoist per-frame values out of closures
    Color innerTextColor = widget.control.getColor("inner_text_color", context) ?? progressBarColors.last;
    String? innerText = widget.control.getString("inner_text");
    int? throttleMs = widget.control.getInt("change_throttle_ms");

    // Local snap function — replaces instance method, avoids re-reading control properties per frame
    int? divisions = widget.control.getInt("divisions");
    double? step = (divisions != null && divisions > 0) ? (max - min) / divisions : null;

    double snapValue(double value) {
      if (step == null) return value;
      return ((value - min) / step!).roundToDouble() * step! + min;
    }

    Widget myControl = SleekCircularSlider(
      min: min,
      max: max,
      initialValue: initialValue.clamp(min, max),
      appearance: CircularSliderAppearance(
        size: sliderSize,
        startAngle: startAngle,
        angleRange: angleRange,
        counterClockwise: counterClockwise,
        animationEnabled: animationEnabled,
        customWidths: CustomSliderWidths(
          trackWidth: trackWidth,
          progressBarWidth: progressBarWidth,
          handlerSize: handlerSize,
        ),
        customColors: CustomSliderColors(
          trackColor: trackColor,
          progressBarColors: progressBarColors,
          dotColor: dotColor,
          shadowColor: shadowColor,
          hideShadow: hideShadow,
        ),
        infoProperties: InfoProperties(
          topLabelText: topLabel ?? '',
          bottomLabelText: bottomLabel ?? '',
          modifier: (double value) {
            String key = _canonicalKey(snapValue(value));
            if (labelMap != null && labelMap.containsKey(key)) {
              return labelMap[key]!;
            }
            return key;
          },
        ),
      ),
      onChange: (double value) {
        double snapped = snapValue(value);
        String key = _canonicalKey(snapped);
        if (throttleMs != null && throttleMs > 0) {
          _onChangeThrottled(snapped, key, throttleMs);
        } else {
          _fireChange(snapped, key);
        }
      },
      onChangeStart: (double value) {
        _lastFiredKey = null;
        widget.control.triggerEvent("change_start", snapValue(value).toString());
      },
      onChangeEnd: (double value) {
        widget.control.triggerEvent("change_end", snapValue(value).toString());
      },
      innerWidget: (double value) {
        double snapped = snapValue(value);
        String key = _canonicalKey(snapped);
        // Label map lookup takes priority
        if (labelMap != null) {
          String displayText = labelMap.containsKey(key) ? labelMap[key]! : key;
          return Center(child: Text(
            displayText,
            style: TextStyle(
              fontSize: sliderSize / 5,
              fontWeight: FontWeight.bold,
              color: innerTextColor,
            ),
          ));
        }
        if (innerText != null) {
          String displayText = innerText.replaceAll("{value}", key);
          return Center(child: Text(
            displayText,
            style: TextStyle(
              fontSize: sliderSize / 8,
              fontWeight: FontWeight.bold,
              color: innerTextColor,
            ),
          ));
        }
        return Center(child: Text(
          key,
          style: TextStyle(
            fontSize: sliderSize / 5,
            fontWeight: FontWeight.bold,
            color: innerTextColor,
          ),
        ));
      },
    );

    return LayoutControl(control: widget.control, child: myControl);
  }
}
