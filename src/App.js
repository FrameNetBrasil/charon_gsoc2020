import React from 'react';
import './App.css';
import Title from './Title';
import Box from './Box';
import Advanced from './Advanced';
import Options from './Options';
import Review from './Review';
import NavBar from './NavBar';
import { Component } from 'react';

class App extends Component{
constructor(props){
    super(props);
    this.state={
        value_key:1
    }
}

    parentFunction=(data_from_child)=>{
        this.setState({value_key:data_from_child});
    }

     
    render(){
        return(
        <div className="App">
	      <header className="App-header">
        <Title/>
	        <hr className="divider"/>
	        <div className="Nav">
	        <NavBar functionCallFromParent={this.parentFunction.bind(this)}/>
	        <hr className="divider1"/>
	        </div>
	        {(() => {
        if (this.state.value_key==3) {
          return (
            <Advanced/>
          )
        } else if (this.state.value_key==2) {
          return (
            <Review/>
          )
        } else {
          return (
            <Options/>
          )
        }
      })()}
	      </header>
	    </div>
        );
    }
}

export default App;

