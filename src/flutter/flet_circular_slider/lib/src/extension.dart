import 'package:flet/flet.dart';
import 'package:flutter/widgets.dart';

import 'flet_circular_slider.dart';

class Extension extends FletExtension {
  @override
  Widget? createWidget(Key? key, Control control) {
    switch (control.type) {
      case "flet_circular_slider":
        return FletCircularSliderControl(control: control);
      default:
        return null;
    }
  }
}
