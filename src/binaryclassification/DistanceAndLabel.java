package graduationprojectclassification;

@SuppressWarnings("rawtypes")
public class DistanceAndLabel implements Comparable {
	double distance;
	boolean label;

	public double getDistance() {
		return distance;
	}

	public boolean getLabel() {
		return label;
	}

	public DistanceAndLabel() {

	}

	public DistanceAndLabel(double distance, boolean label) {
		this.distance = distance;
		this.label = label;

	}

	public static double findDistance(double[] feature1, double[] feature2) {
		double sum = 0;
		for (int i = 0; i < feature1.length; i++) {
			sum += (feature1[i] - feature2[i]) * (feature1[i] - feature2[i]);
		}
		return Math.sqrt(sum);
	}
	
	// implementing compareTo method for customized sorting based on distance.
	public int compareTo(Object obj) {
		double distance1 = this.distance;
		DistanceAndLabel df = (DistanceAndLabel) obj;
		double distance2 = df.distance;
		if (distance1 < distance2)
			return -1;
		else if (distance1 > distance2)
			return 1;
		else
			return -1;

	}
}
