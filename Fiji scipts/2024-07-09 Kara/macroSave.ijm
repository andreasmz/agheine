file1 = File.openDialog("Select the parent file. Its important to select the actual parent file!");
dir1 = File.getParent(file1);
/*dir1 = getDirectory("image")

dir1Ls = getFileList(dir1);
existingFolders = "";
for (i = 0; i < lengthOf(dir1Ls); i++) {
	if (endsWith(dir1Ls[i], "/")) {
		existingFolders += dir1Ls[i] + ", ";
	}
	
}*/

Dialog.create("ImageJ");
Dialog.addMessage("Select a name for the folder for the series files");
Dialog.addString("name", "");
Dialog.show();

folderName = Dialog.getString();
dir2 = dir1+File.separator+folderName+File.separator;

if (File.exists(dir2)) {
	if(getBoolean("The folder already exists. Saving will overide the current files. Do you want to proceed?") != 1) {
		exit();
	}
}
if (lengthOf(folderName)>0) {
	File.makeDirectory(dir1+File.separator+folderName);
	var tiles = getList("image.titles");
	for (i = 0;i < lengthOf(tiles); i++) {
		selectWindow(tiles[i]);
		saveAs("Tiff", dir2+tiles[i]);
	}
}