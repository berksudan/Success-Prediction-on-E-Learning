package graduationprojectclassification;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class Knn {
	public static int KNN_VAL;
	
	@SuppressWarnings("unchecked")
	public static int classify(List<Instance> trainingSet, double[] testFeatures) {
		ArrayList<DistanceAndLabel> distanceLabelList = new ArrayList<>();
		int flag = 0, zeroCount = 0, oneCount = 0;

		for (Instance trainingSample : trainingSet) {
			double dist = DistanceAndLabel.findDistance(trainingSample.getFeatures(), testFeatures);
			DistanceAndLabel DlObject = new DistanceAndLabel(dist, trainingSample.getLabel());
			distanceLabelList.add(DlObject);
			Collections.sort(distanceLabelList);
		}
		while (flag < KNN_VAL) {
			DistanceAndLabel s = distanceLabelList.get(flag);
			boolean label = s.getLabel();
			if (label)
				oneCount++;
			else
				zeroCount++;
			flag++;

		}
		if (zeroCount > oneCount)
			return 0;
		return 1;
	}
}
