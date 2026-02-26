import 'package:flet/flet.dart';
import 'package:flutter/material.dart';
import 'package:sleek_circular_slider/sleek_circular_slider.dart';

class FletCircularSliderControl extends StatelessWidget {
  final Control control;

  const FletCircularSliderControl({
    super.key,
    required this.control,
  });

  @override
  Widget build(BuildContext context) {
    double min = control.getDouble("min", 0)!;
    double max = control.getDouble("max", 100)!;
    double initialValue = control.getDouble("value", 50)!;
    double sliderSize = control.getDouble("size", 150)!;
    double startAngle = control.getDouble("start_angle", 150)!;
    double angleRange = control.getDouble("angle_range", 240)!;
    bool counterClockwise = control.getBool("counter_clockwise", false)!;
    bool animationEnabled = control.getBool("animation_enabled", true)!;

    // Track and bar widths
    double progressBarWidth = control.getDouble("progress_bar_width", sliderSize / 10)!;
    double trackWidth = control.getDouble("track_width", progressBarWidth / 4)!;
    double handlerSize = control.getDouble("handler_size", progressBarWidth / 5)!;

    // Colors
    Color trackColor = control.getColor("track_color", context) ?? const Color(0xFFDCBEFB);
    Color dotColor = control.getColor("dot_color", context) ?? Colors.white;
    Color shadowColor = control.getColor("shadow_color", context) ?? const Color(0xFF2C57C0);
    bool hideShadow = control.getBool("hide_shadow", false)!;

    // Gradient colors for progress bar
    List<Color> progressBarColors = [];
    String? startColor = control.getString("progress_bar_start_color");
    String? endColor = control.getString("progress_bar_end_color");
    if (startColor != null && endColor != null) {
      Color? sc = control.getColor("progress_bar_start_color", context);
      Color? ec = control.getColor("progress_bar_end_color", context);
      if (sc != null && ec != null) {
        progressBarColors = [sc, ec];
      }
    }
    if (progressBarColors.isEmpty) {
      progressBarColors = [const Color(0xFF1E003B), const Color(0xFFEC008A), const Color(0xFF6285DA)];
    }

    // Info properties
    String? topLabel = control.getString("top_label");
    String? bottomLabel = control.getString("bottom_label");

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
            return value.ceil().toString();
          },
        ),
      ),
      onChange: (double value) {
        control.triggerEvent("change", value.toString());
      },
      onChangeStart: (double value) {
        control.triggerEvent("change_start", value.toString());
      },
      onChangeEnd: (double value) {
        control.triggerEvent("change_end", value.toString());
      },
      innerWidget: (double value) {
        String? innerText = control.getString("inner_text");
        if (innerText != null) {
          return Center(child: Text(
            innerText.replaceAll("{value}", value.ceil().toString()),
            style: TextStyle(
              fontSize: sliderSize / 8,
              fontWeight: FontWeight.bold,
              color: control.getColor("inner_text_color", context) ?? progressBarColors.last,
            ),
          ));
        }
        return Center(child: Text(
          value.ceil().toString(),
          style: TextStyle(
            fontSize: sliderSize / 5,
            fontWeight: FontWeight.bold,
            color: control.getColor("inner_text_color", context) ?? progressBarColors.last,
          ),
        ));
      },
    );

    return LayoutControl(control: control, child: myControl);
  }
}
