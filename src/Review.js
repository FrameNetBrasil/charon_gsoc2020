import React, { Component } from 'react';
import './Review.css';

import Box1 from './Box1';
import Modal from './Modal';
import axios from 'axios';
import PropTypes from 'prop-types';
 
import {ScrollBox, ScrollAxes, FastTrack} from 'react-scroll-box';

export class Review extends Component {

  constructor() {
    super();
    this.state = {
      modal: false,
      name: "",
      modalInputName: "",
      text: [],
      modalNew: false,
      modalNewInputName: "",
      custom: "",
      str: "",
      start: "",
      end: "",
      ip: "",
      sid: ""
        }
  }

  componentDidMount()
  {
    axios.get("/server/get_text.php/")
      .then(res => {
        console.log(res);
        const text = res.data;
        this.setState({ text });
      });


    axios.get("/server/show_ip.php/")
      .then(res => {
        console.log(res);
        const ip = res.data;
        this.setState({ ip });
      });

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

  modalNewOpen=(e)=>{
    this.setState({ modalNew: true });
  }

  modalNewClose() {
    this.setState({
      modalNewInputName: "",
      modalNew: false
    });
  }

  handleChange(e) {
    const target = e.target;
    const name = target.name;
    const value = target.value;

    this.setState({
      [name]: value
    });
  }

  saveSentences(e) {
    this.setState({ name: this.state.modalInputName });
    this.modalClose();
    alert("Sentences have been saved successfully.");
  }

  addSentences(e) {
    this.setState({ name: this.state.modalInputName });
    this.modalClose();
    this.modalNewOpen();
  }

  uploadSentences(e)
  {
    this.setState({ name: this.state.modalNewInputName });
    this.modalNewClose();
  }

  get_start_end_ts= (e,val,id1) =>
  {
     e.preventDefault();
     this.str=val;
     var res= val.split("\n");
     var start= res[0];
     var end= res[res.length - 1];
     var sid= id1;
     this.start= start;
     this.end= end;
     this.sid= sid;
     var formData=new FormData();
     formData.append("start_time",this.start);
     formData.append("end_time",this.end);
     formData.append("sid",this.sid);
     var xhr=new XMLHttpRequest();
     var ip= this.state.ip;
     var url= process.env.REACT_APP_FLASK_URI;
     alert(url);
     xhr.open('POST',url,true);
     xhr.send(formData);
  }

handleClick({nativeEvent}) {
      var url= process.env.REACT_APP_FLASK_URI;
      axios.get(url);
  }


  render() {
    return(
      <div className="Review">
      <Box1 />
      <div className="Box1">
      <ul className="menu4">
        {this.state.text.map((t) => (<li><a onClick={ e => this.get_start_end_ts(e, t, this.state.text.indexOf(t)) }>{t}</a></li>))}
      </ul>
      </div>
      <p>Click on a sentence to track objects in that video clip</p>
    <button id="enter" name="Enter" type="submit" value="Enter" onClick={this.modalOpen.bind(this)}>Save Sentences</button>
    <Modal show={this.state.modal} handleClose={e => this.modalClose(e)}>
            <form name="form" enctype="multipart/form-data">
                <label>Are you sure you want to save the sentences? Choose Yes to save and No to add own data</label>
                <br/>
                <input type="button" id="s1" value="Yes" onClick={e=>this.saveSentences(this.state.modalInputName)}/>
                <input type="button" id="s2" value="No" onClick={e=>this.addSentences(this.state.modalInputName)}/>
            </form>
    </Modal>
    <Modal show={this.state.modalNew} handleClose={e => this.modalNewClose(e)}>
            <form name="form" method="post" action={process.env.REACT_APP_API_URI + '/server/uploadSentences.php'} enctype = "multipart/form-data">
                <label>Choose file to upload custom sentences:</label>
                <br/>
                <input type="file" name="custom" id="1"/>
                <br/>
                <input type="submit" id="s3" name="submit" value="Upload"/>
            </form>
    </Modal>
<p className="viewsource">Problems editing? <a className="vs" href="#">View source</a></p>
</div>
    )
  }

}

export default Review;
