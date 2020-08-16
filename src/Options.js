import React, { Component } from 'react';
import './Options.css';
import axios from 'axios';
import ReactDOM from 'react-dom';
import Box from './Box';

export class Options extends Component {

constructor(props) {
    super(props);
 
    this.state = {
      lang: [],
      corp: [],
      doc: [],
      val1: "",
      val2: "",
      filename: "",
      l: "",
      c: "",
      d: "",
      tb1: 0,
      tb2: 0,
      cb: ""
    };

    console.log('** API URL = ' + process.env.REACT_APP_API_URI);
  }

parentFunction=(data_from_child)=>{
        console.log(data_from_child);
        var res1=data_from_child[0];
        var res2=data_from_child[1];
        var res3=data_from_child[2];

        const val1=res1;
        const val2=res2;
        const filename=res3;

        this.setState({ val1 });
        this.setState({ val2 });
        this.setState({ filename });    
    }
    

GetSelectedText(){
        var e1 = document.getElementById("L");
        var res1 = e1.options[e1.selectedIndex].text;

        var e2 = document.getElementById("C");
        var res2 = e2.options[e2.selectedIndex].text;

        var e3 = document.getElementById("D");
        var res3 = e3.options[e3.selectedIndex].text;

        const l=res1;
        const c=res2;
        const d=res3;

        this.setState({ l });
        this.setState({ c });
        this.setState({ d }); 

              
      }

  componentDidMount()
  {
    axios.get('/server/routes.php/')
      .then(res => {
        console.log(res);
        const lang = res.data[0];
         const corp = res.data[1];
          const doc = res.data[2];
        this.setState({ lang });
        this.setState({ corp });
        this.setState({ doc });
      });

    axios.get('/server/settings.php/')
      .then(res => {
        console.log(res);
        const tb1= res.data[0];
        const tb2= res.data[1];
        const cb= res.data[2];
        this.setState({ tb1 });
        this.setState({ tb2 });
        this.setState({ cb });
      });
  }

  render() {
    return(
    	<div className="Options">
      <Box
      functionCallFromParent={this.parentFunction.bind(this)}
      />
    	<p className= "lang">Language</p>
        <div className= "dropdown1" id="d1">
            <select id="L">
            <option key="Select Language">Select Language</option>
            {this.state.lang.map((l) =>
                <option key={l}>{l}</option>
            )}
            </select>
        </div>

        <p className= "corpus">Corpus</p>
        <div className= "dropdown2" id="d2">
            <select id="C">
            <option key="Select Corpus">Select Corpus</option>
            {this.state.corp.map((c) =>
                <option key={c}>{c}</option>
            )}
            </select>
        </div>

        <p className="doc">Document</p>
        <div className="dropdown3" id="d3">
            <select id="D">
            <option key="Select Document">Select Document</option>
            {this.state.doc.map((d) =>
                <option key={d}>{d}</option>
            )}
            </select>
        </div>
        
        <form method="post" action={process.env.REACT_APP_API_URI + '/server/upload.php'}>
        <input
              type="hidden"
              name="n1"
              className="i1"
              value={this.state.val1}
            />
        <input
              type="hidden"
              name="n2"
              className="i2"
              value={this.state.val2}
            />
        <input
              type="hidden"
              name="n3"
              className="i3"
              value={this.state.filename}
            />
        <input
              type="hidden"
              name="n4"
              className="i4"
              value={this.state.l}
            />
        <input
              type="hidden"
              name="n5"
              className="i5"
              value={this.state.c}
            />
        <input
              type="hidden"
              name="n6"
              className="i6"
              value={this.state.d}
            />
        <input
              type="hidden"
              name="n7"
              className="i7"
              value={this.state.tb1}
            />
        <input
              type="hidden"
              name="n8"
              className="i8"
              value={this.state.tb2}
            />
        <input
              type="hidden"
              name="n9"
              className="i9"
              value={this.state.cb}
            />
        <input type="submit" className="Enter" id="enter" value="Upload Files" onClick={this.GetSelectedText.bind(this)}/>
        </form>
        <a className="cancel" href="#">Cancel</a>
        <p className="trythis">Problems uploading? <a className="tt" href="#">Try this</a></p>
        </div>
            )
  }

}

export default Options;