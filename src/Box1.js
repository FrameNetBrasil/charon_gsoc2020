import React, { Component } from 'react';
import './Box1.css';
import axios from 'axios';
import ReactPlayer from 'react-player';

//Get string hash for valid input from user


export class Box1 extends Component {

	 constructor() {
    super();
    this.state = {
      input: ""
        }
  }
  
  captureVideoFrame(video, format, quality) {
        if (typeof video === 'string') {
            video = document.getElementById(video);
        }

        format = format || 'jpeg';
        quality = quality || 0.92;

        if (!video || (format !== 'png' && format !== 'jpeg')) {
            return false;
        }

        var canvas = document.createElement("CANVAS");

        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;

        canvas.getContext('2d').drawImage(video, 0, 0);

        var dataUri = canvas.toDataURL('image/' + format, quality);
        var data = dataUri.split(',')[1];
        var mimeType = dataUri.split(';')[0].slice(5)

        var bytes = window.atob(data);
        var buf = new ArrayBuffer(bytes.length);
        var arr = new Uint8Array(buf);

        for (var i = 0; i < bytes.length; i++) {
            arr[i] = bytes.charCodeAt(i);
        }

        var blob = new Blob([ arr ], { type: mimeType });
        return { blob: blob, dataUri: dataUri, format: format };
    }
    
  render() {

    const url = process.env.REACT_APP_API_URI + '/server/get_output.php';

    return(
    	<div className="Box">
      <ReactPlayer 
      playing
      url={url}
      config={{ file: { attributes: {crossorigin: 'anonymous'}}}}
      width='100%'
      height='100%'
      controls = {true}
      //const frame = captureVideoFrame(this.player.getInternalPlayer())
      />
      </div>
    )
  }

}

export default Box1;