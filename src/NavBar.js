import React, {Component} from 'react';
import { connect } from 'react-redux';
import { Navbar, Nav } from 'react-bootstrap';
import Advanced from './Advanced';
import Options from './Options';
import Review from './Review';

class NavBar extends Component{
    Function1=(e)=>{
        e.preventDefault();
        var x=1;
        this.props.functionCallFromParent(x);
    }
    Function2=(e)=>{
        e.preventDefault();
        var x=2;
        this.props.functionCallFromParent(x);
    }
    Function3=(e)=>{
        e.preventDefault();
        var x=3;
        this.props.functionCallFromParent(x);
    }
    render(){
        return(
        	<Navbar bg="light" variant="light">
      		<Nav className="mr-auto">
        		<Nav.Link href="/" onClick={this.Function1.bind(this)}>Options</Nav.Link>
        		<Nav.Link href="/Review" onClick={this.Function2.bind(this)}>Review</Nav.Link>
        		<Nav.Link href="/Advanced" onClick={this.Function3.bind(this)}>Advanced</Nav.Link>
      		</Nav>
    		</Navbar>
        );
    }
}

export default NavBar;

