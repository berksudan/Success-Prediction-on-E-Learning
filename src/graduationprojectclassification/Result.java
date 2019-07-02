package graduationprojectclassification;

import java.util.List;

public class Result {
	private List<Boolean> realLabels;
	private List<Boolean> predictLabels;
	private int TP, TN, FP, FN;
	private String algorithmName;

	public Result(int algorithmSelection, List<Boolean> realLabelList, List<Boolean> predictedLabelList) {
		this.realLabels = realLabelList;
		this.predictLabels = predictedLabelList;
		TP = TN = FP = FN = 0;
		computeConfusionMatrix();

		algorithmName = "";
		if (algorithmSelection == 1)
			this.algorithmName = "Logistic Regression with Stochastic Gradient Descent";
		else if (algorithmSelection == 2)
			this.algorithmName = "K Nearest Neighbour";
	}

	public double getAccurracy() {
		return (double) (TP + TN) / (TP + TN + FP + FN);
	}

	public double getPrecision() {
		return (double) (TP) / (TP + FP);
	}

	public double getRecall() {
		return (double) (TP) / (TP + FN);
	}

	public double getFMeasure() {
		return (double) (2 * getPrecision() * getRecall()) / (getPrecision() + getRecall());
	}

	private void computeConfusionMatrix() {
		boolean realLabel, predictedLabel;

		for (int i = 0; i < realLabels.size(); i++) {
			realLabel = realLabels.get(i);
			predictedLabel = predictLabels.get(i);

			if (!realLabel && !predictedLabel) // realLabel = 0, predictedLabel = 0.
				TN++;
			else if (!realLabel && predictedLabel) // realLabel = 0, predictedLabel = 1.
				FP++;
			else if (realLabel && !predictedLabel) // realLabel = 1, predictedLabel = 0.
				FN++;
			else // realLabel = 1, predictedLabel = 1.
				TP++;
		}
	}

	public void printConfusionMatrix(String prefixStr) {
		System.out.println(prefixStr + "TP(True Positive)=" + TP + ", FN(False Negative)=" + FN);
		System.out.println(prefixStr + "FP(False Positive)=" + FP + ", TN(True Negative)=" + TN);
	}

	public void printAllResult() {
		System.out.println("-----------------------------------------------");
		System.out.println("RESULT OF " + this.algorithmName + " ALGORITHM:");
		printConfusionMatrix("\t");
		System.out.println("\tAccuracy:" + getAccurracy()*100 + "%");
		System.out.println("\tPrecision:" + getPrecision());
		System.out.println("\tRecall:" + getRecall());
		System.out.println("\tF-Measure:" + getFMeasure());
		System.out.println("-----------------------------------------------");

	}

}
