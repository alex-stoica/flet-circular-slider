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
    widget.control.triggerEvent("change", _canonicalKey(value));
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
    double animDurationMultiplier = widget.control.getDouble("anim_duration_multiplier", 1.0)!;

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
    double shadowWidth = widget.control.getDouble("shadow_width", progressBarWidth * 1.4)!;

    // Colors
    Color trackColor = widget.control.getColor("track_color", context) ?? const Color(0xFFDCBEFB);
    Color dotColor = widget.control.getColor("dot_color", context) ?? Colors.white;
    Color shadowColor = widget.control.getColor("shadow_color", context) ?? const Color(0xFF2C57C0);
    bool hideShadow = widget.control.getBool("hide_shadow", false)!;

    // Disabled mode
    bool disabled = widget.control.getBool("disabled", false)!;

    // Gradient colors for progress bar — multi-color list takes priority
    List<Color> progressBarColors;
    List? rawBarColors = widget.control.get("progress_bar_colors");
    if (rawBarColors != null && rawBarColors.isNotEmpty) {
      ThemeData theme = Theme.of(context);
      progressBarColors = rawBarColors
          .map((c) => parseColor(c.toString(), theme))
          .whereType<Color>()
          .toList();
      if (progressBarColors.isEmpty) {
        progressBarColors = [const Color(0xFF1E003B), const Color(0xFFEC008A), const Color(0xFF6285DA)];
      }
    } else {
      Color? sc = widget.control.getColor("progress_bar_start_color", context);
      Color? ec = widget.control.getColor("progress_bar_end_color", context);
      if (sc != null && ec != null) {
        progressBarColors = [sc, ec];
      } else {
        progressBarColors = [const Color(0xFF1E003B), const Color(0xFFEC008A), const Color(0xFF6285DA)];
      }
    }

    // Info properties
    String? topLabel = widget.control.getString("top_label");
    String? bottomLabel = widget.control.getString("bottom_label");

    // Text styling
    double? innerTextSize = widget.control.getDouble("inner_text_size");
    String? innerTextFontWeight = widget.control.getString("inner_text_font_weight");
    String? innerTextFontFamily = widget.control.getString("inner_text_font_family");
    Color? topLabelColor = widget.control.getColor("top_label_color", context);
    double? topLabelSize = widget.control.getDouble("top_label_size");
    String? topLabelFontWeight = widget.control.getString("top_label_font_weight");
    String? topLabelFontFamily = widget.control.getString("top_label_font_family");
    Color? bottomLabelColor = widget.control.getColor("bottom_label_color", context);
    double? bottomLabelSize = widget.control.getDouble("bottom_label_size");
    String? bottomLabelFontWeight = widget.control.getString("bottom_label_font_weight");
    String? bottomLabelFontFamily = widget.control.getString("bottom_label_font_family");

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
        animDurationMultiplier: animDurationMultiplier,
        customWidths: CustomSliderWidths(
          trackWidth: trackWidth,
          progressBarWidth: progressBarWidth,
          handlerSize: handlerSize,
          shadowWidth: shadowWidth,
        ),
        customColors: CustomSliderColors(
          trackColor: trackColor,
          progressBarColors: progressBarColors,
          dotColor: dotColor,
          shadowColor: shadowColor,
          hideShadow: hideShadow,
        ),
      ),
      onChange: disabled ? null : (double value) {
        double snapped = snapValue(value);
        String key = _canonicalKey(snapped);
        if (throttleMs != null && throttleMs > 0) {
          _onChangeThrottled(snapped, key, throttleMs);
        } else {
          _fireChange(snapped, key);
        }
      },
      onChangeStart: disabled ? null : (double value) {
        _lastFiredKey = null;
        widget.control.triggerEvent("change_start", _canonicalKey(snapValue(value)));
      },
      onChangeEnd: disabled ? null : (double value) {
        widget.control.triggerEvent("change_end", _canonicalKey(snapValue(value)));
      },
      innerWidget: (double value) {
        double snapped = snapValue(value);
        String key = _canonicalKey(snapped);

        // Resolve display text — label_map → inner_text → raw key
        String displayText;
        double defaultFontSize;
        if (labelMap != null) {
          displayText = labelMap.containsKey(key) ? labelMap[key]! : key;
          defaultFontSize = sliderSize / 5;
        } else if (innerText != null) {
          displayText = innerText.replaceAll("{value}", key);
          defaultFontSize = sliderSize / 8;
        } else {
          displayText = key;
          defaultFontSize = sliderSize / 5;
        }

        Text mainText = Text(
          displayText,
          style: TextStyle(
            fontSize: innerTextSize ?? defaultFontSize,
            fontWeight: parseFontWeight(innerTextFontWeight, FontWeight.bold),
            fontFamily: innerTextFontFamily,
            color: innerTextColor,
          ),
        );

        List<Widget> children = [];

        if (topLabel != null && topLabel.isNotEmpty) {
          children.add(Text(
            topLabel,
            style: TextStyle(
              fontSize: topLabelSize ?? 12,
              fontWeight: parseFontWeight(topLabelFontWeight, FontWeight.w600),
              fontFamily: topLabelFontFamily,
              color: topLabelColor ?? Colors.white70,
            ),
          ));
        }

        children.add(mainText);

        if (bottomLabel != null && bottomLabel.isNotEmpty) {
          children.add(Text(
            bottomLabel,
            style: TextStyle(
              fontSize: bottomLabelSize ?? 12,
              fontWeight: parseFontWeight(bottomLabelFontWeight, FontWeight.w600),
              fontFamily: bottomLabelFontFamily,
              color: bottomLabelColor ?? Colors.white70,
            ),
          ));
        }

        return Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: children,
        );
      },
    );

    if (disabled) {
      myControl = Opacity(opacity: 0.5, child: myControl);
    }

    return LayoutControl(control: widget.control, child: myControl);
  }
}
