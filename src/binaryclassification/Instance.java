package graduationprojectclassification;

import java.io.Serializable;

public class Instance implements Serializable {
	private static final long serialVersionUID = 1L;
	private boolean label;
	private double[] features;

	public Instance(boolean label, double[] features) {
		this.setLabel(label);
		this.setFeatures(features);
	}

	public boolean getLabel() {
		return label;
	}

	public void setLabel(boolean label) {
		this.label = label;
	}

	public double[] getFeatures() {
		return features;
	}

	public void setFeatures(double[] features) {
		this.features = features;
	}

	public int getFeatureSize() {
		return features.length;
	}

	public void printInst() {
		System.out.println("----------------------------");
		System.out.println("label:" + label);
		System.out.print("features: ");
		for (double feature : features)
			System.out.print(feature + " ");
		System.out.println("");
	}
}