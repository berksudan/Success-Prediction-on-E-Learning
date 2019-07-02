package programgui;

import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.Font;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.File;
import java.util.concurrent.TimeUnit;

import javax.swing.ImageIcon;
import javax.swing.JButton;
import javax.swing.JComboBox;
import javax.swing.JComponent;
import javax.swing.JFileChooser;
import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTextArea;
import javax.swing.JTextField;
import javax.swing.SwingUtilities;
import javax.swing.UIManager;
import javax.swing.filechooser.FileNameExtensionFilter;

public class SparkGUI extends JFrame {
	private static final long serialVersionUID = 1L;

	private static final String APP_LOGO_RELATIVE_PATH = ".app_logo.png";
	private JPanel sparkContentPanel;

	private static final String LABELING_METHODS[] = { "Threshold Labeling", "KMeans Labeling" };
	private JButton buttonPVBrowseDataset, buttonVVBrowseDataset, buttonBrowsePy, buttonPreprocess;
	private JComboBox<String> labelingMethodPicker;
	private JTextField selectedPVDataset, selectedVVDataset, selectedPyFile;

	private JTextArea outputPreprocessTextArea;
	private SparkMenuBar menubar;
	JFrame outputFrame;

	public SparkGUI() {
		super("Web Log Data Preprocessor with Apache Spark 4.3.3");
		initAttributes();
		setDefaultIcon(APP_LOGO_RELATIVE_PATH);

		adjustFrameSize();
		adjustMenuBar();

		configureComponents();
		setLocationRelativeTo(null);
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		this.setContentPane(sparkContentPanel);
		setVisible(true);

	}

	private void setDefaultIcon(String iconRelativePath) {
		String iconFullPath = System.getProperty("user.dir") + "/" + iconRelativePath;
		ImageIcon img = new ImageIcon(iconFullPath);
		System.out.println(iconFullPath);
		this.setIconImage(img.getImage());
	}

	private void adjustFrameSize() {
		Dimension constantDimension = new Dimension(500, 300);
		setSize(constantDimension);
		setResizable(false);
	}

	private void configureComponents() {

		buttonPVBrowseDataset.setAlignmentX(CENTER_ALIGNMENT);
		buttonPVBrowseDataset.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent arg0) {
				selectedPVDataset.setText(openFileInBrowser());
			}
		});
		selectedPVDataset.setEditable(false);
		selectedPVDataset.setFont(new Font("Arial", Font.BOLD, 11));
		// -------------------------------------------------------------------

		buttonVVBrowseDataset.setAlignmentX(CENTER_ALIGNMENT);
		buttonVVBrowseDataset.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent arg0) {
				selectedVVDataset.setText(openFileInBrowser());
			}
		});
		selectedVVDataset.setEditable(false);
		selectedVVDataset.setFont(new Font("Arial", Font.BOLD, 11));
		// -------------------------------------------------------------------

		buttonBrowsePy.setAlignmentX(CENTER_ALIGNMENT);
		buttonBrowsePy.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent arg0) {
				selectedPyFile.setText(openFileInBrowser());
			}
		});
		buttonPreprocess.setAlignmentX(CENTER_ALIGNMENT);
		buttonPreprocess.setForeground(Color.RED);
		buttonPreprocess.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				runPreprocessOperation();
			}
		});

		selectedPyFile.setEditable(false);
		selectedPyFile.setFont(new Font("Arial", Font.BOLD, 11));

	}

	private void adjustMenuBar() {
		menubar.addMenu("Info", new String[] { "This Program is implemented\n by Berk Sudan and Simay Sanlı." });
		menubar.addMenu("Date", new String[] { "June 2019" });
		menubar.addMenu("Version", new String[] { "v1.0" });
		this.setJMenuBar(menubar);

	}

	private void initAttributes() {
		outputFrame = new JFrame("Program Output");
		outputPreprocessTextArea = new JTextArea();
		menubar = new SparkMenuBar();

		// For Page-Views
		selectedPVDataset = new JTextField("Chosen_PV_Dataset");
		buttonPVBrowseDataset = new JButton("Browse Page-Views Dataset...");
		// For Video-Views
		selectedVVDataset = new JTextField("Chosen_VV_Dataset");
		buttonVVBrowseDataset = new JButton("Browse Video-Views Dataset...");

		buttonBrowsePy = new JButton("Browse Py File...");
		buttonPreprocess = new JButton("Preprocess Data");

		selectedPyFile = new JTextField("Chosen_Py_Preprocessor");
		labelingMethodPicker = new JComboBox<>(LABELING_METHODS);
		sparkContentPanel = new SparkPanel(
				new JComponent[] { selectedPVDataset, buttonPVBrowseDataset, selectedVVDataset, buttonVVBrowseDataset,
						selectedPyFile, buttonBrowsePy, labelingMethodPicker, buttonPreprocess });

	}

	private void executeBashScript(SparkBashScript hbs) {
		int commandCounter = 0;
		String bashScriptText = hbs.getBashScript();
		String[] bashScriptCommands = bashScriptText.split("\\n");
		String commandOutput = new String("");

		for (String command : bashScriptCommands) {
			outputPreprocessTextArea
					.append(String.format("[%d] COMMAND IS EXECUTED: <<%s>>\n", commandCounter, command));
			outputPreprocessTextArea.update(outputPreprocessTextArea.getGraphics());
			commandOutput = SparkBashScript.runBashCommand(command);
			if (!commandOutput.isEmpty()) {
				outputPreprocessTextArea.append("OUTPUT:\n" + commandOutput);
				outputPreprocessTextArea.update(outputPreprocessTextArea.getGraphics());
			}
			outputPreprocessTextArea.append("------------------------------------------------\n");
			commandCounter++;
		}
	}

	private SparkBashScript obtainBashScript() {
		String pyFile = selectedPyFile.getText().toString();
		boolean useKMeans = labelingMethodPicker.getSelectedIndex() == 1;
		String inputPVDataset = selectedPVDataset.getText().toString();
		String inputVVDataset = selectedVVDataset.getText().toString();
		String mergedFileTargetDir = extractUpperFolder(inputPVDataset);
		boolean areFilesZipped = inputVVDataset.endsWith((".zip"));

		System.out.println("Python File: " + "<<" + pyFile + ">>");
		System.out.println("Use KMeans: " + "<<" + useKMeans + ">>");
		System.out.println("Input Page-View Dataset: " + "<<" + inputPVDataset + ">>");
		System.out.println("Input Video-View Dataset: " + "<<" + inputVVDataset + ">>");
		System.out.println("Merged File Dataset: " + "<<" + mergedFileTargetDir + ">>");
		System.out.println("Input Files Are Zipped: " + "<<" + areFilesZipped + ">>");

		return new SparkBashScript(pyFile, useKMeans, inputPVDataset, inputVVDataset, mergedFileTargetDir,
				areFilesZipped);
	}

	private void runPreprocessOperation() {

		outputPreprocessTextArea.setText("Waiting for the result...\n");
		try {
			TimeUnit.SECONDS.sleep(2);
		} catch (InterruptedException e) {
			e.printStackTrace();
		}

		JScrollPane scrollPane = new JScrollPane(outputPreprocessTextArea);
		JFrame outputFrame = new JFrame("Preprocess Output");
		outputFrame.getContentPane().add(scrollPane, BorderLayout.CENTER);
		outputFrame.setSize(new Dimension(900, 700));
		outputFrame.setLocationRelativeTo(null);// center the frame
		outputFrame.setVisible(true);// make it visible to the user

		SparkBashScript hbs = obtainBashScript();
		executeBashScript(hbs);
	}

	private String openFileInBrowser() {
		JFileChooser fileChooser = new JFileChooser();
		fileChooser.setCurrentDirectory(new File(System.getProperty("user.dir")));
		fileChooser.setFileSelectionMode(JFileChooser.FILES_ONLY);
		fileChooser.setAcceptAllFileFilterUsed(true);
		fileChooser.addChoosableFileFilter(new FileNameExtensionFilter("CSV Documents", "csv"));
		fileChooser.addChoosableFileFilter(new FileNameExtensionFilter("Jar Files", "jar"));

		int result = fileChooser.showOpenDialog(this);
		if (result == JFileChooser.APPROVE_OPTION) {
			File selectedFile = fileChooser.getSelectedFile();
			return selectedFile.getAbsolutePath();
		} else {
			return "File is not recognized";
		}
	}

	private String extractUpperFolder(String aStr) {
		String upperFolder = "";
		String fileDelimeter = "/";
		String[] splittedString = aStr.split(fileDelimeter);
		for (int i = 0; i < splittedString.length - 2; i++)
			upperFolder += splittedString[i] + fileDelimeter;
		return upperFolder;
	}

	public static void main(String[] args) {
		try {
			UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName());
		} catch (Exception e) {
			e.printStackTrace();
		}
		SwingUtilities.invokeLater(new Runnable() {
			public void run() {
				new SparkGUI();
			}
		});
	}

}
