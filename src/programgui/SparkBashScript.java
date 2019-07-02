package programgui;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class SparkBashScript {
	private String bashCommand;
	
	private String pyPath;
	private boolean useKMeans;
	private String pageViewsfullPath, videoViewsfullPath;
	private String mergedFileTargetDir;
	private boolean inputFilesAreZipped;

	public SparkBashScript(String pyPath,boolean useKMeans, String pageViewsfullPath, String videoViewsfullPath,
			String mergedFileTargetDir, boolean inputFilesAreZipped) {
		this.pyPath = pyPath;
		this.useKMeans = useKMeans;
		this.pageViewsfullPath = pageViewsfullPath;
		this.videoViewsfullPath = videoViewsfullPath;
		this.mergedFileTargetDir = mergedFileTargetDir;
		this.inputFilesAreZipped = inputFilesAreZipped;
		this.bashCommand = constructBashCommand();
	}

	private String constructBashCommand() {
		StringBuilder sb = new StringBuilder();
		sb.append("python3 ");
		sb.append(pyPath + " ");
		sb.append(useKMeans ? "1 " : "0 ");
		sb.append(pageViewsfullPath + " ");
		sb.append(videoViewsfullPath + " ");
		sb.append(mergedFileTargetDir + " ");
		sb.append(inputFilesAreZipped ? "1 " : "0 ");
		sb.append("\n");
		return sb.toString();
	}

	public static String runBashCommand(String command) {
		Process process;
		BufferedReader reader;
		StringBuilder output = new StringBuilder();
		ProcessBuilder processBuilder = new ProcessBuilder();

		processBuilder.command("bash", "-c", command);
		try {
			process = processBuilder.start();
			reader = new BufferedReader(new InputStreamReader(process.getInputStream()));

			String line;
			while ((line = reader.readLine()) != null)
				output.append(line + "\n");

			process.waitFor();

		} catch (IOException e) {
			e.printStackTrace();
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
		return output.toString();
	}

	public String getBashScript() {
		return bashCommand;
	}
}
