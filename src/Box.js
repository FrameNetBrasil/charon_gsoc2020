import React, { Component } from 'react';
import upload_cloud from "./upload_cloud.JPG"
import './Box.css'
import sha256 from 'crypto-js/sha256';
import {ProgressBar} from 'react-bootstrap';
import Trigger1 from './Trigger1';
import Trigger2 from './Trigger2';
import Modal from './Modal';
import axios from 'axios';

//Get string hash for valid input from user

export class Box extends Component {

	 constructor() {
    super();
    this.state = {
      modal: false,
      name: "",
      modalInputName: "",
      modal1: false,
      name1: "",
      modalInputName1: "",
      chk: "",
      uploadPercentage: 0
        }
  }

    sha1(s) {

        var sha1_hash = sha256(s);
        alert("SHA1 hash is:" + sha1_hash);
    }

    download(x) {
        var userInput = x;
        var val1="1";
        var filename=x;
        this.alertUserInput(userInput);
        var val2=this.parseUrl(userInput);
        this.props.functionCallFromParent([val1,val2,filename]);
        this.modalClose();
    }

    alertUserInput(ui) {

        alert(ui);
    }

    parseUrl(ui) {
        var regExp = /^(?:https?:\/\/)?(?:www\.)?(?:youtu\.be\/|youtube\.com\/(?:embed\/|v\/|watch\?v=|watch\?.+&v=))((\w|-){11})(?:\S+)?$/,
            match = ui.match(regExp);
        alert(match ? "Valid Youtube URL" : "Invalid URL");
        var val=0;
        if (match)
        {
            this.sha1(ui);
            return "1";
        }
        else 
        	return "0";
    }

    upload(x,y) {
        var uploadInput = x;
        var val1="2";
        var filename=y;
        this.alertUploadSuccess(uploadInput);
        var val2=this.checkFormat(uploadInput);
        this.props.functionCallFromParent([val1,val2,filename]);
        this.modalClose1();
    }

    getExtension(ui) {
        var parts = ui.split('.');
        return parts[parts.length - 1];
    }

    uploadProgress = ({ target: { files } }) =>{
    console.log( files[0] )
    let data = new FormData();
    data.append( 'file', files[0] )

    const options = {
      onUploadProgress: (progressEvent) => {
        const {loaded, total} = progressEvent;
        let percent = Math.floor( (loaded * 100) / total )
        console.log( `${loaded}kb of ${total}kb | ${percent}%` );

        if( percent < 100 ){
          this.setState({ uploadPercentage: percent })
        }
      }
    }

    axios.post("https://run.mocky.io/v3/6e275dcd-d92a-4acc-bf1f-7f2ceec29ff2", data, options).then(res => { 
        console.log(res)
        this.setState({ avatar: res.data.url, uploadPercentage: 100 }, ()=>{
          setTimeout(() => {
            this.setState({ uploadPercentage: 0 })
          }, 1000);
        })
    })
  }


    isVideo(ui) {
        var ext = this.getExtension(ui);
        switch (ext.toLowerCase()) {
            case 'm4v':
            case 'avi':
            case 'mpg':
            case 'mp4':
            case 'mkv':
                // etc
                return true;
        }
        return false;
    }

    checkFormat(ui) {
        if (!this.isVideo(ui)) {
            alert("Invalid File Format. Please upload a video file.");
            return "0";
        } else {
            this.sha1(ui);
            return "1";
        }
    }

    alertUploadSuccess(ui) {
        alert(ui);
    }

  handleChange(e) {
    const target = e.target;
    const name = target.name;
    const value = target.value;

    this.setState({
      [name]: value
    });
  }

  getInput(e) {
    this.setState({ name: this.state.modalInputName });
    this.modalClose();
  }

  modalOpen=(e)=>{
  	e.preventDefault();
    this.setState({ modal: true });
  }

  modalClose() {
    this.setState({
      modalInputName: "",
      modal: false
    });
  }

  uploadFile(e) {
    this.setState({ name: this.state.modalInputName1 });
    this.modalClose1();
  }

  modalOpen1=(e)=>{
  	e.preventDefault();
    this.setState({ modal1: true });
  }

  modalClose1() {
    this.setState({
      modalInputName1: "",
      modal1: false
    });
  }
    
  
  render() {
    return(

    	<div>
    	<div className="Box">
    	<img src={upload_cloud} width="150" height="100" alt="upload_cloud"/>
    	<p>Select files <a id="url" className="ftw" href="#" onClick={this.modalOpen.bind(this)}>from the web</a> or <a id="local" className="fyc" href="#" onClick={this.modalOpen1.bind(this)}>from your computer</a></p>
        <Modal show={this.state.modal} handleClose={e => this.modalClose(e)}>
        <form name="form" enctype="multipart/form-data">
            <label>Enter Video URL:</label>
            <input
              type="text"
              name="modalInputName"
              onChange={e => this.handleChange(e)}
              className="form-control"
            />
            <input type="button" id="s1" value="Submit" onClick={e=>this.download(this.state.modalInputName)}/>
        </form>
        </Modal>
        <Modal show={this.state.modal1} handleClose={e => this.modalClose1(e)}>
        <form name="form" enctype="multipart/form-data">
            <label>Choose file to upload:</label>
            <input type="file" name="chk" onChange={this.uploadProgress}/>
            { this.state.uploadPercentage > 0 && <ProgressBar now={this.state.uploadPercentage} active label={`${this.state.uploadPercentage}%`} /> }
            <br/>
            <label>Enter file path:</label>
            <input
              type="text"
              name="modalInputName1"
              onChange={e => this.handleChange(e)}
              className="form-control"
            />
            <input type="button" id="s" value="Upload" onClick={e=>this.upload(this.state.chk,this.state.modalInputName1)}/>
        </form>
        </Modal>
        </div>
	</div>
    )
  }

}

export default Box;