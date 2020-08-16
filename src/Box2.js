import React, { Component } from 'react';
import './Box2.css';
import axios from 'axios';

//Get string hash for valid input from user

export class Box2 extends Component {

	 constructor() {
    super();
    this.state = {
      data: ""
        }
  }
  
  componentWillMount() {
    axios.get('/server/upload.php/')
      .then(res => {
        console.log(res);
        const data = res.data;
        this.setState({ data });
      });
  }
    
  render() {

    return(
    	<div className="Box2">
      <p>{this.state.data}</p>
      </div>
    )
  }

}

export default Box2;