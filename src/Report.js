
import './Report.css';
import axios from 'axios';
import React, { Component } from 'react';
import {Route} from 'react-router-dom';

export class Report extends Component{ 
    constructor(props)
    {
        super(props);
        this.state={
            option:"",
        }
    }

    GetOption=(e,val)=>
    {
     e.preventDefault();
     this.val= val;
     var formData=new FormData();
     formData.append("val",this.val);
     var xhr=new XMLHttpRequest();
     xhr.open('POST','http://127.0.0.1:5000/report',true);
     xhr.send(formData);
    }
    
    handleClick({nativeEvent}) {
      var url= 'http://127.0.0.1:5000';
      axios.get(url);
  }

   render()
   {
        return(
        <div className='overlay2'>
        <h4 className='h5'>Reports</h4>
        <hr className="divider2"/>
        <div className="Box6">
        <p className="rt">Choose the type of report to generate from the below options:</p>
        <div>
        <p className="o1">1. Frames annotated in text and in the video per corpus</p>
        <input className="r1" type="submit" value="Show Report" onClick={e =>this.GetOption(e,"1")}/>
        </div>
        <div>
        <p className="o2">2. Frames annotated in text and in the video per document</p>
        <input className="r2" type="submit" value="Show Report" onClick={e =>this.GetOption(e,"2")}/>
        </div>
        <div>
        <p className="o3">3. Frames annotated in text and in the video per sentence</p>
        <input className="r3" type="submit" value="Show Report" onClick={e =>this.GetOption(e,"3")}/>
        </div>
        <div>
        <p className="o4">4. Frames and Frame Elements annotated in text and in the video per corpus</p>
        <input className="r4" type="submit" value="Show Report" onClick={e =>this.GetOption(e,"4")}/>
        </div>
        <div>
        <p className="o5">5. Frames and Frame Elements annotated in text and in the video per document</p>
        <input className="r5" type="submit" value="Show Report" onClick={e =>this.GetOption(e,"5")}/>
        </div>
        <div>
        <p className="o6">6. Frames and Frame Elements annotated in text and in the video per sentence</p>
        <input className="r6" type="submit" value="Show Report" onClick={e =>this.GetOption(e,"6")}/>
        </div>
        <div>
        <p className="o7">7. Frames annotated in text and in the video according to the (a)sychronicity in the corpus</p>
        <input className="r7" type="submit" value="Show Report" onClick={e =>this.GetOption(e,"7")}/>
        </div>
        <div>
        <p className="o8">8. Frames annotated in text and in the video according to the (a)sychronicity in the document</p>
        <input className="r8" type="submit" value="Show Report" onClick={e =>this.GetOption(e,"8")}/>
        </div>
        <div>
        <p className="o9">9. Frames annotated in text and in the video according to the (a)sychronicity in the sentence.</p>
        <input className="r9" type="submit" value="Show Report" onClick={e =>this.GetOption(e,"9")}/>
        </div>
        <div>
        <p className="o10">10. Frames and Frame Elements annotated in text and in the video according to the (a)sychronicity in the corpus.</p>
        <input className="r10" type="submit" value="Show Report" onClick={e =>this.GetOption(e,"10")}/>
        </div>
        <div>
        <p className="o11">11. Frames and Frame Elements annotated in text and in the video according to the (a)sychronicity in the document.</p>
        <input className="r11" type="submit" value="Show Report" onClick={e =>this.GetOption(e,"11")}/>
        </div>
        <div>
        <p className="o12">12. Frames and Frame Elements annotated in text and in the video according to the (a)sychronicity in the sentence.</p>
        <input className="r12" type="submit" value="Show Report" onClick={e =>this.GetOption(e,"12")}/>
        </div>
        <div>
        <p className="o13">13. YOLO recognized objects matching Frames and Frame Elements in the bounding boxes per corpus</p>
        <input className="r13" type="submit" value="Show Report" onClick={e =>this.GetOption(e,"13")}/>
        </div>
        <div>
        <p className="o14">14. YOLO recognized objects matching Frames and Frame Elements in the bounding boxes per document</p>
        <input className="r14" type="submit" value="Show Report" onClick={e =>this.GetOption(e,"14")}/>
        </div>
        <div>
        <p className="o15">15. YOLO recognized objects matching Frames and Frame Elements in the bounding boxes per sentence</p>
        <input className="r15" type="submit" value="Show Report" onClick={e =>this.GetOption(e,"15")}/>
        </div>
        <div>
        <p className="o16">16. Ternary Qualia Relations connecting an LU in the text with any of the LUs in a frame annotated in the video.</p>
        <input className="r16" type="submit" value="Show Report" onClick={e =>this.GetOption(e,"16")}/>
        </div>
        </div>
        </div>
        )
    }
}

export default Report;
