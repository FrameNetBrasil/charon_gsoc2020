import React, {Component} from 'react';
import { connect } from 'react-redux';
import { Navbar, Nav } from 'react-bootstrap';

class NavBar1 extends Component{
    render(){
        return(
            <Navbar bg="light" variant="light">
            <Nav className="mr-auto">
                <Nav.Link href="#">Report 1</Nav.Link>
                <Nav.Link href="#">Report 2</Nav.Link>
                <Nav.Link href="#">Report 3</Nav.Link>
                <Nav.Link href="#">Report 4</Nav.Link>
                <Nav.Link href="#">Report 5</Nav.Link>
                <Nav.Link href="#">Report 6</Nav.Link>
            </Nav>
            </Navbar>
        );
    }
}

export default NavBar1;
