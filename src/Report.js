
import './Report.css';
import axios from 'axios';
import PropTypes from 'prop-types';
import React, { Component } from 'react';
import {Route} from 'react-router-dom';
import NavBar1 from './NavBar1';
import DropdownTreeSelect from 'react-dropdown-tree-select'
import 'react-dropdown-tree-select/dist/styles.css'



export class Report extends Component{ 
    constructor(props)
    {
        super(props);
        this.state={
            val:"",
            s:"",
            c:"",
            d:"",
            corp:[],
            doc:[],
            sent:[],
            corpid:[],
            docid:[],
            output:"",
        }
    }


    handleClick({nativeEvent}) {
      var url= process.env.REACT_APP_FLASK_URI+"/report";
      axios.get(url);
  }

   componentDidMount()
  {
    axios.get('/server/leftPane.php/')
      .then(res => {
        console.log(res);
        const corp = res.data[0];
        const doc = res.data[1];
        const sent = res.data[2];
        const corpid = res.data[3];
        const docid = res.data[4];
        this.setState({corp});
        this.setState({doc});
        this.setState({sent});
        this.setState({corpid});
        this.setState({docid});
      });
  }

getReport()
{
  axios.get('http://localhost:5000/report')
    .then(res => {
        console.log(res);
      });
}

 onChange = (currentNode, selectedNodes) => {
  console.log('onChange::', currentNode, selectedNodes)
  var res=selectedNodes[0].value;
  if(this.state.corpid.includes(res))
    this.val="1";
  else if(this.state.docid.includes(res))
    this.val="2";
  else if(this.state.sent.includes(res))
    this.val="3";
  //var formData=new FormData();
  //formData.append("val",this.val);
  //formData.append("Id",res);
  //var xhr=new XMLHttpRequest();
  //xhr.open('POST','http://127.0.0.1:5000/report',true);
  //xhr.send(formData);

  axios.post(process.env.REACT_APP_FLASK_URI+"/report", {
      val: this.val,
      Id: res,
})
.then((response) => {
     console.log(response.data); 
     var op=JSON.stringify(response.data);
     var op1=op.replace(/:{/g, ":\n{");
     var op101=op1.replace(/[0-9]:/g, '');
     var op2=op101.replace(/['\[\]"}]+/g, '')
     var op3=op2.replace(/,/g,",\n");
     var op4=op3.replace(/[{]+/g, '');
     var op5=op4.replace(/corpusEntry/g, '\tcorpusEntry');
     var op6=op5.replace(/corpusName/g, '\tcorpusName');
     var op7=op6.replace(/idCorpus/g, '\tidCorpus');
     var op8=op7.replace(/documentEntry/g, '\tdocumentEntry');
     var op9=op8.replace(/documentName/g, '\tdocumentName');
     var op10=op9.replace(/idDocument/g, '\tidDocument');
     var op11=op10.replace(/idSentence/g, '\n\tidSentence');
     var op12=op11.replace(/SentenceText/g, '\tSentenceText');
     var op13=op12.replace(/Ternary_Qualia_Relations/g, '\tTernary_Qualia_Relations');
     var op14=op13.replace(/Lexical Unit in Sentence/g, '\t\t\tLexical Unit in Sentence');
     var op15=op14.replace(/Frame:frm/g, '\t\t\tFrame:frm');
     var op16=op15.replace(/Relations to LUs/g, '\t\t\tRelations to LUs');
     var op17=op16.replace(/Qualia Relation/g, '\t\t\t\tQualia Relation');
     var op18=op17.replace(/Lexical Unit in Frame/g, '\n\t\t\t\tLexical Unit in Frame');
     var op19=op18.replace(/textFrames/g, '\ttextFrames');
     var op20=op19.replace(/videoFrames/g, '\n\tvideoFrames');
     var op21=op20.replace(/frameEntry/g, '\t\tframeEntry');
     var op22=op21.replace(/frameName/g, '\t\tframeName');
     var op23=op22.replace(/idFrame/g, '\n\t\tidFrame');
     var op24=op23.replace(/startTime/g, '\t\tstartTime');
     var op25=op24.replace(/endTime/g, '\t\tendTime');
     var op26=op25.replace(/fes/g, '\t\tfes');
     var op27=op26.replace(/idFrameElement/g, '\t\tidFrameElement');
     var op28=op27.replace(/frameElementEntry/g, '\t\t\t\tframeElementEntry');
     var op29=op28.replace(/frameElementName/g, '\t\t\t\tframeElementName');
     var op30=op29.replace(/1:/g, '\n***Frames annotated in text and in the video***');
     var op31=op30.replace(/2:/g, '\n***Frames and Frame Elements annotated in text and in the video***');
     var op32=op31.replace(/3:/g, '\n***Frames annotated in text and in the video according to the (a)sychronicity***');
     var op33=op32.replace(/4:/g, '\n***Frames and Frame Elements annotated in text and in the video according to the (a)sychronicity***');
     var op34=op33.replace(/5:/g, '\n***YOLO recognized objects matching Frames and Frame Elements in the bounding boxes***');
     var output=op34.replace(/6:/g, '\n***Ternary qualia relations connecting an LU in the text with any of the LUs in a frame annotated in the video***');
     this.setState({output});
});

}


 onAction = (node, action) => {
  console.log('onAction::', action, node)
}
 onNodeToggle = currentNode => {
  console.log('onNodeToggle::', currentNode)
}

   render()
   {


var children2=[]
this.state.sent.forEach((n, i) => { children2[i] = {label: "Sentence "+this.state.sent[i],value: this.state.sent[i],} })
var children1=[]
this.state.doc.forEach((n, i) => { children1[i] = {label: this.state.doc[i],value: this.state.docid[i],children: children2} })
var start=[]
this.state.corp.forEach((n, i) => { start[i] = {label: this.state.corp[i],value: this.state.corpid[i],children: children1} })



var data = start
 
        return(
        <div className='overlay2'>
        <h4 className='h5'>Multimodal Corpus Annotation Report</h4>
        <hr className="divider2"/>
        <div className="Box6">
        <DropdownTreeSelect className="dds" data={data} onChange={this.onChange} onAction={this.onAction} onNodeToggle={this.onNodeToggle} />
        <input type="submit" className="Submit" id="enter" value="Show Reports" onClick={this.getReport}/>
        </div>
        <div className="Box7">
        <NavBar1/>
        <div className="Box8">
        <pre>{this.state.output}</pre>
        </div>
        </div>
        </div>
        )
    }
}

export default Report;
