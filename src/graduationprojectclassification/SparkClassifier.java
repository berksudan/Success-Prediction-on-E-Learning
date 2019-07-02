package graduationprojectclassification;

import java.util.ArrayList;
import java.util.List;

public class SparkClassifier {
	private final String DATASET_DIR, DATASET_FILE;
	private final int K_FOLD_VAL;

	private List<Instance> allDataList;
	private SparkFacade sparkFacade;

	private List<Instance> createTestDataset(int testIndex, List<List<Instance>> splittedDatasetList) {
		List<Instance> testDataset = new ArrayList<Instance>();
		testDataset.addAll(splittedDatasetList.get(testIndex));
		return testDataset;
	}

	private List<Instance> createTrainingDataset(int testIndex, List<List<Instance>> splittedDatasetList) {
		List<Instance> trainingDataset = new ArrayList<Instance>();
		for (int j = 0; j < splittedDatasetList.size(); j++)
			if (testIndex != j)
				trainingDataset.addAll(splittedDatasetList.get(j));
		return trainingDataset;
	}

	private List<Boolean> constructRealLabelList(List<Instance> allDataList) {
		List<Boolean> realLabelList = new ArrayList<>();
		for (Instance anInstance : allDataList)
			realLabelList.add(anInstance.getLabel());
		return realLabelList;
	}

	public SparkClassifier(int kFoldVal, String datasetDirectory, String datasetFileName, boolean isLogOpen) {
		this.K_FOLD_VAL = kFoldVal;
		this.DATASET_DIR = datasetDirectory;
		this.DATASET_FILE = datasetFileName;

		this.sparkFacade = new SparkFacade("SparkClassifierProgram", "local", isLogOpen);
		sparkFacade.init();
		this.allDataList = sparkFacade.loadDataset(this.DATASET_DIR + this.DATASET_FILE);
	}

	private void runLogisticRegression(int lrIterationNum, double lrThreshold) {
		LogisticRegressionSGD.THRESHOLD = lrThreshold;
		LogisticRegressionSGD.ITERATION_NUM = lrIterationNum;
		runSparkClassifier(1);
	}

	private void runKNN(int knnVal) {
		Knn.KNN_VAL = knnVal;
		runSparkClassifier(2);
	}

	public void runSparkClassifier(int algorithmSelection) {
		List<Instance> trainingDataset, testDataset;
		List<Boolean> realLabelList = constructRealLabelList(allDataList);
		List<Boolean> predictLabelList = new ArrayList<>();
		List<List<Instance>> splittedDatasetList = CrossValidation.splitData(K_FOLD_VAL, allDataList);
		List<Boolean> predictTestDatasetLabel = new ArrayList<>();

		for (int i = 0; i < K_FOLD_VAL; i++) {
			// split train and test data for each k-fold value.
			trainingDataset = createTrainingDataset(i, splittedDatasetList);
			testDataset = createTestDataset(i, splittedDatasetList);

			if (algorithmSelection == 1) { // Selected Algorithm: <Logistic regression>
				sparkFacade.trainDatawithLR(trainingDataset);
				predictTestDatasetLabel = LogisticRegressionSGD.testData(testDataset);
			} else if (algorithmSelection == 2) // Selected Algorithm: <KNN>
				predictTestDatasetLabel = sparkFacade.kNNClassify(trainingDataset, testDataset);

			predictLabelList.addAll(predictTestDatasetLabel);
		}
		Result result = new Result(algorithmSelection, realLabelList, predictLabelList);
		result.printAllResult();

		sparkFacade.stop();
	}

	public static void main(String[] args) {
		int kFoldVal = 5;
		String datasetDirectory = "labeled_datasets/";
		String datasetFileName = "real_labeled_dataset1.csv";
		boolean isLogOpen = true;

		SparkClassifier sparkClassifier = new SparkClassifier(kFoldVal, datasetDirectory, datasetFileName, isLogOpen);

		int knnVal;
		
		boolean useKNN = false;
		if (useKNN) {
			knnVal = 3;
			sparkClassifier.runKNN(knnVal);
		} else {
			int lrIterationNum = 100;
			double lrThreshold = 0.5;
			sparkClassifier.runLogisticRegression(lrIterationNum, lrThreshold);
		}

	}

}
