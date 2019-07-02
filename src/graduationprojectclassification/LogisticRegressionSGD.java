package graduationprojectclassification;

import java.util.ArrayList;
import java.util.List;

public class LogisticRegressionSGD {
	public static int ITERATION_NUM;
	public static double THRESHOLD;
	
	private static double sigmoid(double x) {
		return 1.0 / (1.0 + Math.exp(-x));
	}

	public static double predictLabel(int weightsLength, double[] feature, double[] W) {
		double score = 0;
		for (int i = 0; i < weightsLength; i++)
			score += feature[i] * W[i];
		return sigmoid(score);
	}

	public static List<Boolean> testData(List<Instance> testDataList) {
		List<Boolean> predictLabelList = new ArrayList<>();
		double[] lastWeights = LogRegWeightUpdater.getCurrentWeights();
		for (int i = 0; i < testDataList.size(); i++) {
			Instance inst = testDataList.get(i);
			double predictValue = predictLabel(inst.getFeatureSize(), inst.getFeatures(), lastWeights);
			predictLabelList.add(predictValue > THRESHOLD);
		}
		return predictLabelList;
	}

}
