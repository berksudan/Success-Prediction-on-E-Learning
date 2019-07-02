package graduationprojectclassification;

import java.util.ArrayList;
import java.util.List;
import org.apache.log4j.Level;
import org.apache.log4j.Logger;
import org.apache.spark.SparkConf;
import org.apache.spark.api.java.JavaRDD;
import org.apache.spark.api.java.JavaSparkContext;

public final class SparkFacade {
	private SparkConf config;
	private static JavaSparkContext sc;
	private JavaRDD<Instance> allData;// our data
	private List<Instance> allDataList;

	public SparkFacade(String appName, String master, boolean isLogOpen) {
		if (!isLogOpen) {
			Logger.getLogger("org").setLevel(Level.OFF);
			Logger.getLogger("akka").setLevel(Level.OFF);
		}
		config = new SparkConf().setAppName(appName).setMaster(master);
	}

	// Initializes the spark context
	public void init() {
		sc = new JavaSparkContext(config);
	}

	// Stops the spark context
	public void stop() {
		sc.close();
	}

	public List<Instance> loadDataset(String path) {
		JavaRDD<String> data = sc.textFile(path);
		allData = data.map(line -> createLabeledPoint(line));
		allData.cache();
		allDataList = allData.collect();
		return allDataList;

	}

	public List<Instance> getAllDataList() {
		return allDataList;
	}

	// update weight operation with logistic regression in train data
	public void trainDatawithLR(List<Instance> trainingDataList) {
		int numOfIterations = LogisticRegressionSGD.ITERATION_NUM;
		
		new LogRegWeightUpdater(trainingDataList.get(0).getFeatureSize(), 0.0001, 0);
		Instance instance = new Instance(false, trainingDataList.get(0).getFeatures());
		for (int i = 0; i < numOfIterations; i++) {
			JavaRDD<Instance> trainingDataCopy = sc.parallelize(trainingDataList);
			instance = trainingDataCopy.reduce(LogRegWeightUpdater::updateWeight);
			LogRegWeightUpdater.updateWeight(instance, instance);
		}
	}

	// KNN Algorithm
	public List<Boolean> kNNClassify(List<Instance> trainingDataList, List<Instance> testDataList) {
		List<Boolean> predictLabelList = new ArrayList<>();
		for (int i = 0; i < testDataList.size(); i++) {
			double[] testFeatures = testDataList.get(i).getFeatures();
			int predictLabel = Knn.classify(trainingDataList, testFeatures);
			predictLabelList.add(predictLabel == 1);
		}
		return predictLabelList;

	}

	private static Instance createLabeledPoint(String line) {
		String[] all_attributes;
		boolean label;
		double[] input_features;
		all_attributes = line.split(","); // Csv-Separator = ","
		input_features = new double[all_attributes.length - 1];
		for (int i = 0; i < all_attributes.length - 1; i++)
			input_features[i] = Double.parseDouble(all_attributes[i]);
		// 0:fail, 1:success
		label = Integer.parseInt(all_attributes[all_attributes.length - 1]) == 1;// last index is a label
		return new Instance(label, input_features);
	}

}