package graduationprojectclassification;

import java.util.ArrayList;
import java.util.List;

public class CrossValidation {
	public static List<List<Instance>> splitData(int kFoldVal, List<Instance> totalInstances) {
		ArrayList<List<Instance>> sampleDataList = new ArrayList<List<Instance>>();

		int total_size = totalInstances.size();
		int average = total_size / kFoldVal;
		int index = 0;
		for (int i = 0; i < kFoldVal; i++) {
			List<Instance> currentList = new ArrayList<Instance>();
			for (int j = index; j < average + index; j++) {
				currentList.add(totalInstances.get(j));
			}
			index = index + average;
			sampleDataList.add(currentList);
		}
		return sampleDataList;
	}
}
