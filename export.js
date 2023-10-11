const writeToTextFile = (text, fileName) => {
    let textFile = null;
    const makeTextFile = (text) => {
      const data = new Blob([text], {
        type: 'text/plain',
      });
      if (textFile !== null) {
        window.URL.revokeObjectURL(textFile);
      }
      textFile = window.URL.createObjectURL(data);
      return textFile;
    };
    const link = document.createElement('a');
    link.setAttribute('download', fileName);
    link.href = makeTextFile(text);
    link.click();
  };
  
//   const data = 'Learning how to write in a file.';
//   writeToTextFile(data, 'output.txt');
