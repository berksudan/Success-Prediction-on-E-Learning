package programgui;

import java.awt.Color;
import java.awt.Font;

import javax.swing.JMenu;
import javax.swing.JMenuBar;
import javax.swing.JMenuItem;

public class SparkMenuBar extends JMenuBar {
	private static final long serialVersionUID = 1L;
	private static final Font defaultFont = new Font("Arial", Font.BOLD, 11);
	private static final Color defaultColor = new Color(51, 51, 0);

	public SparkMenuBar() {
		super();
		setFont(defaultFont);
		setBackground(defaultColor);

	}

	public void addMenu(String menuCaption, String[] menuItems) {
		JMenu newMenu = new JMenu(menuCaption);

		for (String menuItemText : menuItems) {
			JMenuItem newMenuItem = new JMenuItem(menuItemText);
			newMenu.add(newMenuItem);
			this.add(newMenu);
		}
	}
}
