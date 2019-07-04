package graduationprojectclassification;

public class LogRegWeightUpdater {
	private static double[] currentWeights;
	private static double gradientDescentRate;

	public static double[] getCurrentWeights() {
		return currentWeights;
	}

	public LogRegWeightUpdater(int numOfFeatures, double rate, double initialWeightValue) {
		LogRegWeightUpdater.gradientDescentRate = rate;
		LogRegWeightUpdater.currentWeights = new double[numOfFeatures];
		for (int i = 0; i < numOfFeatures; i++)
			LogRegWeightUpdater.currentWeights[i] = initialWeightValue;
	}

	public static Instance updateWeight(Instance i1, Instance i2) { // Process i1, return i2
		double[] features = i1.getFeatures();
		boolean label = i1.getLabel();
		int intLabel = label ? 1 : 0;
		double predicted = LogisticRegressionSGD.predictLabel(currentWeights.length, features, currentWeights);
		// update weights with stochastic gradient descent
		for (int j = 0; j < currentWeights.length; j++) {
			currentWeights[j] += gradientDescentRate * (intLabel - predicted) * predicted * (1 - predicted) * features[j];
		}
		return i2;
	}

}
