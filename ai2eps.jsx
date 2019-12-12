// Save AI as EPS
var destFolder, sourceFolder, files, sourceDoc, saveOpts, targetFile;
saveOpts = new EPSSaveOptions();
saveOpts.pdfCompatible = true;
saveOpts.embedAllFonts = true;

sourceFolder = Folder.selectDialog('Select a folder to convert all AI files to EPS in it.'); 

if ( sourceFolder != null )
{
	// var files = find_files (sourceFolder, ['.ai']);
	files = new Array();
	files = sourceFolder.getFiles( '*.ai' )	
	if (files.length > 0) 
	{
		destFolder = Folder.selectDialog( 'Select a folder where to save converted EPS files.' );
		for ( i = 0; i < files.length; i++ ) 
		{
			sourceDoc = app.open(files[i]);			
			targetFile = getNewName();
			sourceDoc.saveAs( targetFile, saveOpts );
			sourceDoc.close();
		}
		alert( files.length + ' file(s) processed' );
	}
	else 
	{
		alert('No AI files found.');
	}
}

function getNewName()
{
	var ext, docName, newName, saveInFile;
	docName = sourceDoc.name;
	ext = '.eps'; 
	newName = "";
	for ( var i = 0 ; docName[i] != "." ; i++ )
	{
		newName += docName[i];
	}
	newName += ext; 
	saveInFile = new File( destFolder + '/' + newName );
	return saveInFile;
}

// function find_files (dir, mask_array){
//   var arr = [];
//   for (var i = 0; i < mask_array.length; i++){
//     arr = arr.concat (find_files_sub (dir, [], mask_array[i].toUpperCase()));
//   }
//   return arr;
// }

// function find_files_sub (dir, array, mask){
//   var f = Folder (dir).getFiles ( '*.*' );
//   for (var i = 0; i < f.length; i++){
//     if (f[i] instanceof Folder){
//       find_files_sub (f[i], array, mask);
//     } else if (f[i].name.substr (-mask.length).toUpperCase() == mask){
//             array.push (f[i]);
//     }
//   }
//   return array;
// }