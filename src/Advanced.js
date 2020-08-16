
import React, { Component } from 'react';
import './Advanced.css';
import Box2 from './Box2';


export class Advanced extends Component {

constructor(props) {
    super(props);
 
    this.state = {
      tb1:"720",
      tb2:"480",
    };
  }


  handleChange(e, field) {
    this.setState({
      [field]: e.target.value
    });
  }

  render() {
    return(
    	<div className="Advanced">
      <Box2/>
    	<p className="caption">Drop files smaller than</p>
    	<p className="l1">Min. Width</p>
    	<p className="l2">Min. Height</p>
      <form method="post" action= "{process.env.REACT_APP_API_URI}/server/settings.php/" enctype = "multipart/form-data">
    	<input className="tb1" name="tb1" type="text" value={this.state.tb1} onChange={e => this.handleChange(e,"tb1")}/>
    	<input className="tb2" name="tb2" type="text" value={this.state.tb2} onChange={e => this.handleChange(e,"tb2")}/>
    	<input className="cb" name="cb" type="checkbox" defaultChecked="checked"/>
    	<p className="ct" name="ct">Create Thumbnails</p>
      <input type="submit" id="enter" className="Enter" value="Save Settings" />
      </form>
      <p className="eventlog">Want to dig deeper? <a className="el" href="#">Open event log</a></p>
      </div>
    )
  }

}

export default Advanced;