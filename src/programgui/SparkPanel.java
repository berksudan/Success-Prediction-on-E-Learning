package programgui;

import java.awt.Color;

import javax.swing.BoxLayout;
import javax.swing.JComponent;
import javax.swing.JPanel;

public class SparkPanel extends JPanel {
	private static final long serialVersionUID = 1L;

	public SparkPanel(JComponent[] componentList) {
		super();

		setLayout(null);
		setBackground(Color.MAGENTA);// Default Background Color
		setBounds(55, 55, 400, 150); // Default Bound values
		setLayout(new BoxLayout(this, BoxLayout.Y_AXIS));


		for (JComponent component : componentList)
			addPanel(component);

	}

	public void addPanel(JComponent aJComponent) {
		add(aJComponent);
	}

}
