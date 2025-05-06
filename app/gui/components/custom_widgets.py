"""
Custom widgets for PyQt/PySide6 applications.
Includes sliding menus and animated stack widgets.
"""
from PySide6.QtCore import (
    QPropertyAnimation, QEasingCurve, QParallelAnimationGroup,
    QSequentialAnimationGroup, Qt, Property, QPoint, QSize, Signal
)
from PySide6.QtWidgets import (
    QWidget, QStackedWidget, QGraphicsOpacityEffect, QFrame
)
from PySide6.QtGui import QIcon, QPalette, QBrush, QColor, QPixmap
class SlideMenu(QWidget):
    """A custom sliding menu widget that can expand and collapse."""
    
    # Signal emitted when menu state changes
    stateChanged = Signal(bool)  # True for expanded, False for collapsed
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._expanded = False
        self._default_width = 0
        self._expanded_width = 200
        self._animation_duration = 500
        self._easing_curve = QEasingCurve.Type.Linear
        self._toggle_button = None
        self._toggle_button_icons = None
        self.setAutoFillBackground(True)
        
    def setup(self, default_width=0, expanded_width=200, 
              animation_duration=500, easing_curve=QEasingCurve.Type.Linear,
              background_color = None):
        """Configure the sliding menu."""
        self._default_width = default_width
        self._expanded_width = expanded_width
        self._animation_duration = animation_duration
        self._easing_curve = easing_curve
        
        # Set initial width
        self.setFixedWidth(self._default_width)
        if background_color:
            self.setStyleSheet(f"background-color: {background_color};")

        self.set_background_color(background_color)
        
        self.setStyleSheet(f"""
        
        QWidget {{
            background-color: {background_color};
        }}
        
        QPushButton {{
            text-align: left;
            padding: 10px 14px;
            border-radius: 8px;
            margin: 2px 5px;
            color: #F7FAFC;
            background-color: #4A5568;
        }}
        
        QPushButton:hover {{
            background-color: #3B82C4;
            padding-left: 20px;
            color: white;
            border-left: 4px solid #E6F0FA;
        }}
        """)

    def set_background_color(self, color):
        """Set the background color of the menu using the palette."""
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor(color))
        self.setPalette(palette)
        
    def set_toggle_button(self, button, collapsed_icon=None, expanded_icon=None):
        """Set the button that toggles this menu."""
        self._toggle_button = button
        self._toggle_button_icons = (collapsed_icon, expanded_icon)
        
        # Connect the button's clicked signal to toggle function
        if button:
            button.clicked.connect(self.toggle)
            
            # Set the initial icon if icons are provided
            if collapsed_icon and not self._expanded:
                button.setIcon(collapsed_icon)
                
    def toggle(self):
        """Toggle between expanded and collapsed states."""
        if self._expanded:
            self.collapse()
        else:
            self.expand()
    
    def expand(self):
        """Expand the menu."""
        self._animate_width(self._expanded_width)
        self._expanded = True
        self.stateChanged.emit(True)
        
        # Change icon if available
        if self._toggle_button and self._toggle_button_icons and self._toggle_button_icons[1]:
            self._toggle_button.setIcon(self._toggle_button_icons[1])
    
    def collapse(self):
        """Collapse the menu."""
        self._animate_width(self._default_width)
        self._expanded = False
        self.stateChanged.emit(False)
        
        # Change icon if available
        if self._toggle_button and self._toggle_button_icons and self._toggle_button_icons[0]:
            self._toggle_button.setIcon(self._toggle_button_icons[0])
    
    def _animate_width(self, target_width):
        """Animate the width change of the menu."""
        self.animation = QPropertyAnimation(self, b"minimumWidth")
        self.animation.setStartValue(self.width())
        self.animation.setEndValue(target_width)
        self.animation.setDuration(self._animation_duration)
        self.animation.setEasingCurve(self._easing_curve)
        self.animation.start()
        
        self.animation2 = QPropertyAnimation(self, b"maximumWidth")
        self.animation2.setStartValue(self.width())
        self.animation2.setEndValue(target_width)
        self.animation2.setDuration(self._animation_duration)
        self.animation2.setEasingCurve(self._easing_curve)
        self.animation2.start()
        
    def is_expanded(self):
        """Return True if the menu is expanded, False otherwise."""
        return self._expanded


class AnimatedStackedWidget(QStackedWidget):
    """A custom stacked widget with page transition animations."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._animations = {}
        self._current_anim = None
        self._animation_type = "slide"
        self._animation_duration = 500
        self._easing_curve = QEasingCurve.Type.OutBack
        self._direction = Qt.Orientation.Horizontal
        
    def setup(self, animation_type="slide", duration=500, 
              easing=QEasingCurve.Type.OutBack, direction=Qt.Orientation.Horizontal):
        """Configure the animated stack widget."""
        self._animation_type = animation_type
        self._animation_duration = duration
        self._easing_curve = easing
        self._direction = direction
        
    def set_navigation(self, button_page_map):
        """Connect buttons to pages for navigation.
        
        Args:
            button_page_map: Dictionary mapping button objects to page indices or names
        """
        for button, page in button_page_map.items():
            if isinstance(page, str):
                # Find the page index by name
                for i in range(self.count()):
                    if self.widget(i).objectName() == page:
                        page_index = i
                        break
                else:
                    raise ValueError(f"Page '{page}' not found")
            else:
                page_index = page
                
            # Connect the button to switch to this page
            button.clicked.connect(lambda checked=False, idx=page_index: self.slide_to_index(idx))
            
    def slide_to_index(self, index):
        """Animate the transition to the specified page index."""
        if index == self.currentIndex() or index < 0 or index >= self.count():
            return
            
        # If there's already an animation in progress, stop it
        if self._current_anim and self._current_anim.state() == QPropertyAnimation.Running:
            self._current_anim.stop()
            
        # Get the current and next widget
        current_widget = self.currentWidget()
        next_widget = self.widget(index)
        
        if not current_widget or not next_widget:
            return
            
        # Set the next widget visible but at the right position
        next_widget.setVisible(True)
        
        if self._animation_type == "slide":
            self._slide_animation(current_widget, next_widget, index)
        elif self._animation_type == "fade":
            self._fade_animation(current_widget, next_widget, index)
        else:
            # Default to no animation
            self.setCurrentIndex(index)
            
    def _slide_animation(self, current_widget, next_widget, next_index):
        """Create and start a slide animation between widgets."""
        # Determine direction of animation
        forward = next_index > self.currentIndex()
        
        # Position the next widget
        if self._direction == Qt.Orientation.Horizontal:
            offset = self.width()
            current_start = QPoint(0, 0)
            current_end = QPoint(-offset if forward else offset, 0)
            next_start = QPoint(offset if forward else -offset, 0)
            next_end = QPoint(0, 0)
        else:  # Vertical
            offset = self.height()
            current_start = QPoint(0, 0)
            current_end = QPoint(0, -offset if forward else offset)
            next_start = QPoint(0, offset if forward else -offset)
            next_end = QPoint(0, 0)
            
        # Position widgets for animation
        next_widget.setGeometry(current_widget.geometry())
        next_widget.move(next_start)
        
        # Create the animation group
        anim_group = QParallelAnimationGroup(self)
        
        # Animation for the current widget
        current_anim = QPropertyAnimation(current_widget, b"pos")
        current_anim.setStartValue(current_start)
        current_anim.setEndValue(current_end)
        current_anim.setDuration(self._animation_duration)
        current_anim.setEasingCurve(self._easing_curve)
        
        # Animation for the next widget
        next_anim = QPropertyAnimation(next_widget, b"pos")
        next_anim.setStartValue(next_start)
        next_anim.setEndValue(next_end)
        next_anim.setDuration(self._animation_duration)
        next_anim.setEasingCurve(self._easing_curve)
        
        # Add animations to the group
        anim_group.addAnimation(current_anim)
        anim_group.addAnimation(next_anim)
        
        # Connect to update the current index when animation finishes
        anim_group.finished.connect(lambda: self._animation_finished(next_index))
        
        # Start the animation
        self._current_anim = anim_group
        anim_group.start()
        
    def _fade_animation(self, current_widget, next_widget, next_index):
        """Create and start a fade animation between widgets."""
        # Create opacity effects for both widgets
        current_effect = QGraphicsOpacityEffect(current_widget)
        next_effect = QGraphicsOpacityEffect(next_widget)
        
        current_widget.setGraphicsEffect(current_effect)
        next_widget.setGraphicsEffect(next_effect)
        
        # Set initial opacity
        current_effect.setOpacity(1.0)
        next_effect.setOpacity(0.0)
        
        # Position the next widget on top
        next_widget.setGeometry(current_widget.geometry())
        next_widget.raise_()
        next_widget.setVisible(True)
        
        # Create the animation group
        anim_group = QParallelAnimationGroup(self)
        
        # Animation for fading out the current widget
        fade_out = QPropertyAnimation(current_effect, b"opacity")
        fade_out.setStartValue(1.0)
        fade_out.setEndValue(0.0)
        fade_out.setDuration(self._animation_duration)
        fade_out.setEasingCurve(self._easing_curve)
        
        # Animation for fading in the next widget
        fade_in = QPropertyAnimation(next_effect, b"opacity")
        fade_in.setStartValue(0.0)
        fade_in.setEndValue(1.0)
        fade_in.setDuration(self._animation_duration)
        fade_in.setEasingCurve(self._easing_curve)
        
        # Add animations to the group
        anim_group.addAnimation(fade_out)
        anim_group.addAnimation(fade_in)
        
        # Connect to update the current index when animation finishes
        anim_group.finished.connect(lambda: self._animation_finished(next_index))
        
        # Start the animation
        self._current_anim = anim_group
        anim_group.start()
        
    def _animation_finished(self, index):
        """Cleanup after animation finished."""
        # Set the final index
        self.setCurrentIndex(index)
        
        # Reset all widget positions and effects
        for i in range(self.count()):
            widget = self.widget(i)
            if widget and i != index:
                widget.setVisible(False)
                widget.move(0, 0)
                widget.setGraphicsEffect(None)
        
        # Clear the current animation
        self._current_anim = None


class ButtonGroup:
    """Manages a group of buttons with active/inactive styling."""
    
    def __init__(self):
        self._buttons = []
        self._active_style = ""
        self._inactive_style = ""
        self._current_active = None
        
    def setup(self, buttons, active_style, inactive_style):
        """Configure the button group.
        
        Args:
            buttons: List of QPushButton objects
            active_style: CSS style string for active button
            inactive_style: CSS style string for inactive buttons
        """
        self._buttons = buttons
        self._active_style = active_style
        self._inactive_style = inactive_style
        
        # Set initial styles
        for button in buttons:
            button.setStyleSheet(self._inactive_style)
            button.clicked.connect(lambda checked=False, btn=button: self.set_active(btn))
            
    def set_active(self, active_button):
        """Set the specified button as active and others as inactive."""
        for button in self._buttons:
            if button == active_button:
                button.setStyleSheet(self._active_style)
                self._current_active = button
            else:
                button.setStyleSheet(self._inactive_style)

"""
class StyleLoader:
    #Utility class to apply styles to widgets
    
    @staticmethod
    def load_json_style(window, ui, json_file_path):
       
        import json
        from pathlib import Path
        
        # Read the JSON file
        with open(json_file_path, 'r') as f:
            style_data = json.load(f)
            
        # Apply QPushButtonGroup settings
        if 'QPushButtonGroup' in style_data:
            for group_config in style_data['QPushButtonGroup']:
                buttons = []
                for button_name in group_config['Buttons']:
                    if hasattr(ui, button_name):
                        buttons.append(getattr(ui, button_name))
                        
                if buttons and 'Style' in group_config:
                    style_info = group_config['Style'][0]
                    active_style = style_info.get('Active', '')
                    inactive_style = style_info.get('NotActive', '')
                    
                    button_group = ButtonGroup()
                    button_group.setup(buttons, active_style, inactive_style)
                    
                    # Store the button group in the window
                    window._button_group = button_group
                    
        # Apply QCustomSlideMenu settings
        if 'QCustomSlideMenu' in style_data:
            for menu_config in style_data['QCustomSlideMenu']:
                menu_name = menu_config.get('name')
                if hasattr(ui, menu_name):
                    menu_widget = getattr(ui, menu_name)
                    
                    if not isinstance(menu_widget, SlideMenu):
                        print(f"Warning: {menu_name} is not a SlideMenu instance")
                        continue
                        
                    # Get configuration values
                    default_size = menu_config.get('defaultSize', [{}])[0].get('width', 0)
                    expanded_size = menu_config.get('expandedSize', [{}])[0].get('width', 200)
                    
                    anim_config = menu_config.get('menuTransitionAnimation', [{}])[0]
                    duration = anim_config.get('animationDuration', 500)
                    easing_name = anim_config.get('animationEasingCurve', 'Linear')
                    easing_curve = getattr(QEasingCurve.Type, easing_name, QEasingCurve.Type.Linear)
                    
                    # Setup the menu
                    menu_widget.setup(
                        default_width=default_size,
                        expanded_width=expanded_size,
                        animation_duration=duration,
                        easing_curve=easing_curve
                    )
                    
                    # Set up toggle button if specified
                    toggle_config = menu_config.get('toggleButton', [{}])[0]
                    btn_name = toggle_config.get('buttonName')
                    
                    if btn_name and hasattr(ui, btn_name):
                        toggle_button = getattr(ui, btn_name)
                        
                        # Get icons if specified
                        icons_config = toggle_config.get('icons', [{}])[0]
                        collapsed_icon_path = icons_config.get('whenMenuIsCollapsed')
                        expanded_icon_path = icons_config.get('whenMenuIsExpanded')
                        
                        collapsed_icon = QIcon(collapsed_icon_path) if collapsed_icon_path else None
                        expanded_icon = QIcon(expanded_icon_path) if expanded_icon_path else None
                        
                        menu_widget.set_toggle_button(toggle_button, collapsed_icon, expanded_icon)
        
        # Apply QStackedWidget settings
        if 'QStackedWidget' in style_data:
            for widget_name, config in style_data['QStackedWidget'].items():
                if hasattr(ui, widget_name):
                    stacked_widget = getattr(ui, widget_name)
                    
                    if not isinstance(stacked_widget, AnimatedStackedWidget):
                        print(f"Warning: {widget_name} is not an AnimatedStackedWidget instance")
                        continue
                        
                    # Get transition settings
                    transition = config.get('transition', {})
                    anim_type = transition.get('type', 'slide')
                    duration = transition.get('duration', 500)
                    easing_name = transition.get('easing', 'OutBack')
                    direction_name = transition.get('direction', 'horizontal')
                    
                    # Convert string values to enum values
                    easing_curve = getattr(QEasingCurve.Type, easing_name, QEasingCurve.Type.OutBack)
                    direction = Qt.Orientation.Horizontal if direction_name == 'horizontal' else Qt.Orientation.Vertical
                    
                    # Setup the widget
                    stacked_widget.setup(
                        animation_type=anim_type,
                        duration=duration,
                        easing=easing_curve,
                        direction=direction
                    )
                    
                    # Setup navigation if specified
                    nav_config = config.get('navigation', {})
                    if nav_config:
                        button_page_map = {}
                        for btn_name, page_name in nav_config.items():
                            if hasattr(ui, btn_name) and isinstance(page_name, str):
                                button_page_map[getattr(ui, btn_name)] = page_name
                                
                        stacked_widget.set_navigation(button_page_map)
"""