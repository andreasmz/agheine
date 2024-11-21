var path1 = r"C:\YOUR\WORKING\FOLDER";
var file1 = r"YOUR_FILENAME.file"

file1 = File.openDialog("Select a LIF file");
dir1 = File.getParent(file1);
s = "open=["+file1+"] autoscale color_mode=Default open_all_series rois_import=[ROI manager] view=Hyperstack stack_order=XYCZT";

run("Bio-Formats Importer", s);


tiles = getList("image.titles");

for (i = 0;i < lengthOf(tiles); i++) {
	//print(tiles[i]);
	selectWindow(tiles[i]);
	for (c = 1; c <= 3; c++) {
		Stack.setChannel(c);
		resetMinAndMax();
		run("Enhance Contrast", "saturated=0.35");
	}
	Stack.setChannel(1);
	//pathSave = dir+File.separator+tiles[i]+".tif";
	//saveAs("Tiff", pathSave);
	
}