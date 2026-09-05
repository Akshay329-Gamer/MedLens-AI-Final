import os
import json
import base64
import re
import requests

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import HTMLResponse


app = FastAPI(title="MedLens — AI Clinical Insight")


HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<meta name="description" content="MedLens AI clinical information structuring tool">
<title>MedLens — AI Clinical Intelligence</title>

<style>
*{box-sizing:border-box}

:root{
    --bg:#03040d;
    --panel:#071020;
    --panel2:#0a1529;
    --line:rgba(83,221,255,.20);
    --text:#f1f7ff;
    --muted:#8da3bd;
    --cyan:#25e7ff;
    --blue:#4d8dff;
    --violet:#a855f7;
    --purple:#7c3aed;
    --green:#39f2ae;
    --yellow:#ffd166;
    --red:#ff5577;
    --shadow:0 25px 80px rgba(0,0,0,.45)
}

html{scroll-behavior:smooth}

body{
    margin:0;
    font-family:Inter,"Segoe UI",Arial,sans-serif;
    color:var(--text);
    background:
        radial-gradient(circle at 8% 8%,rgba(37,231,255,.13),transparent 24%),
        radial-gradient(circle at 92% 12%,rgba(168,85,247,.16),transparent 25%),
        radial-gradient(circle at 50% 95%,rgba(77,141,255,.12),transparent 35%),
        var(--bg);
    min-height:100vh;
    overflow-x:hidden
}

body:before{
    content:"";
    position:fixed;
    inset:0;
    pointer-events:none;
    background-image:
        linear-gradient(rgba(100,180,255,.025) 1px,transparent 1px),
        linear-gradient(90deg,rgba(100,180,255,.025) 1px,transparent 1px);
    background-size:40px 40px;
    mask-image:linear-gradient(to bottom,black,transparent 92%)
}

body:after{
    content:"";
    position:fixed;
    width:420px;
    height:420px;
    right:-180px;
    top:280px;
    border-radius:50%;
    border:1px solid rgba(168,85,247,.12);
    box-shadow:
        0 0 100px rgba(168,85,247,.08),
        inset 0 0 100px rgba(37,231,255,.05);
    pointer-events:none
}

.header{
    position:relative;
    border-bottom:1px solid rgba(83,221,255,.14);
    padding:22px 20px 24px;
    background:rgba(3,6,18,.78);
    backdrop-filter:blur(22px);
    z-index:2
}

.header-inner{
    max-width:1160px;
    margin:auto;
    display:flex;
    align-items:center;
    justify-content:space-between;
    gap:20px
}

.brand{
    display:flex;
    align-items:center;
    gap:14px
}

.logo{
    width:56px;
    height:56px;
    display:grid;
    place-items:center;
    border-radius:18px;
    background:
        linear-gradient(135deg,rgba(37,231,255,.16),rgba(168,85,247,.20));
    border:1px solid rgba(37,231,255,.40);
    box-shadow:
        0 0 35px rgba(37,231,255,.12),
        inset 0 0 25px rgba(168,85,247,.08);
    font-size:27px
}

h1{
    margin:0;
    font-size:34px;
    letter-spacing:-1.2px;
    line-height:1
}

h1 .cyan{color:var(--cyan)}
h1 .violet{color:var(--violet)}

.header p{
    margin:7px 0 0;
    color:var(--muted);
    font-size:12px;
    letter-spacing:.3px
}

.system-status{
    display:flex;
    align-items:center;
    gap:8px;
    padding:9px 14px;
    border-radius:30px;
    border:1px solid rgba(57,242,174,.20);
    background:rgba(57,242,174,.045);
    color:var(--green);
    font-size:10px;
    font-weight:900;
    letter-spacing:.7px
}

.status-dot{
    width:7px;
    height:7px;
    border-radius:50%;
    background:var(--green);
    box-shadow:0 0 12px var(--green)
}

.hero{
    max-width:1160px;
    margin:0 auto;
    padding:48px 20px 24px;
    display:grid;
    grid-template-columns:1fr;
    gap:18px
}

.hero-kicker{
    display:inline-flex;
    width:max-content;
    align-items:center;
    gap:8px;
    padding:7px 12px;
    border:1px solid rgba(168,85,247,.35);
    border-radius:30px;
    background:rgba(168,85,247,.07);
    color:#c99aff;
    font-size:10px;
    font-weight:900;
    letter-spacing:1px
}

.hero h2{
    max-width:850px;
    margin:16px 0 8px;
    font-size:clamp(34px,6vw,60px);
    line-height:1.02;
    letter-spacing:-2.4px
}

.hero h2 span{
    background:linear-gradient(90deg,var(--cyan),#72a5ff,var(--violet));
    -webkit-background-clip:text;
    background-clip:text;
    color:transparent
}

.hero-text{
    max-width:760px;
    margin:0;
    color:var(--muted);
    font-size:15px;
    line-height:1.7
}

.pipeline{
    display:flex;
    align-items:center;
    gap:0;
    margin-top:20px;
    overflow-x:auto;
    padding-bottom:4px
}

.step{
    display:flex;
    align-items:center;
    gap:8px;
    white-space:nowrap;
    color:#7189a6;
    font-size:10px;
    font-weight:800
}

.step-number{
    width:27px;
    height:27px;
    display:grid;
    place-items:center;
    border-radius:50%;
    border:1px solid rgba(83,221,255,.25);
    background:rgba(83,221,255,.05);
    color:var(--cyan);
    font-size:11px
}

.step-line{
    width:45px;
    height:1px;
    background:linear-gradient(90deg,rgba(37,231,255,.35),rgba(168,85,247,.35));
    margin:0 10px
}

.container{
    max-width:1160px;
    margin:0 auto;
    padding:0 20px
}

.card{
    position:relative;
    margin-bottom:20px;
    padding:26px;
    border-radius:22px;
    background:
        linear-gradient(145deg,rgba(9,22,43,.90),rgba(5,10,24,.92));
    border:1px solid var(--line);
    box-shadow:var(--shadow);
    backdrop-filter:blur(20px);
    overflow:hidden
}

.card:before{
    content:"";
    position:absolute;
    top:0;
    left:30px;
    right:30px;
    height:1px;
    background:linear-gradient(
        90deg,
        transparent,
        var(--cyan),
        var(--violet),
        transparent
    );
    opacity:.7
}

.card:after{
    content:"";
    position:absolute;
    width:130px;
    height:130px;
    right:-70px;
    top:-70px;
    border-radius:50%;
    background:radial-gradient(circle,rgba(168,85,247,.10),transparent 68%);
    pointer-events:none
}

.title{
    display:flex;
    align-items:center;
    gap:12px;
    margin-bottom:20px
}

.icon{
    width:42px;
    height:42px;
    display:grid;
    place-items:center;
    border-radius:13px;
    background:
        linear-gradient(135deg,rgba(37,231,255,.10),rgba(168,85,247,.13));
    border:1px solid rgba(83,221,255,.20);
    box-shadow:0 0 22px rgba(37,231,255,.06);
    font-size:18px
}

h3{
    margin:0;
    font-size:18px
}

.sub{
    margin-top:4px;
    color:var(--muted);
    font-size:12px
}

.grid{
    display:grid;
    grid-template-columns:repeat(2,1fr);
    gap:15px
}

.full{grid-column:1/-1}

label{
    display:block;
    margin-bottom:7px;
    color:#b8cae0;
    font-size:10px;
    font-weight:900;
    letter-spacing:.8px
}

input,textarea,select{
    width:100%;
    padding:13px 14px;
    border:1px solid rgba(126,166,210,.16);
    border-radius:12px;
    outline:none;
    background:rgba(1,7,18,.72);
    color:var(--text);
    font-size:13px;
    transition:.2s
}

input::placeholder,
textarea::placeholder{
    color:#526981
}

input:focus,
textarea:focus,
select:focus{
    border-color:rgba(37,231,255,.60);
    box-shadow:
        0 0 0 3px rgba(37,231,255,.07),
        0 0 25px rgba(37,231,255,.05)
}

input:focus-visible,
textarea:focus-visible,
select:focus-visible,
button:focus-visible,
.file-label:focus-visible{
    outline:2px solid var(--cyan);
    outline-offset:3px
}

select option{background:#081326}

textarea{
    min-height:78px;
    resize:vertical
}

.upload{
    padding:34px 20px;
    text-align:center;
    border:1px dashed rgba(37,231,255,.42);
    border-radius:17px;
    background:
        radial-gradient(circle at 50% 30%,rgba(37,231,255,.08),transparent 45%),
        radial-gradient(circle at 70% 90%,rgba(168,85,247,.07),transparent 45%),
        rgba(2,8,19,.55);
    transition:.25s
}

.upload:hover{
    border-color:rgba(168,85,247,.65);
    box-shadow:inset 0 0 35px rgba(37,231,255,.035)
}

.upload-icon{
    width:62px;
    height:62px;
    margin:0 auto 12px;
    display:grid;
    place-items:center;
    border-radius:20px;
    background:linear-gradient(135deg,rgba(37,231,255,.12),rgba(168,85,247,.14));
    border:1px solid rgba(83,221,255,.22);
    font-size:27px
}

.upload strong{
    display:block;
    font-size:15px
}

.upload p{
    margin:6px 0;
    color:var(--muted);
    font-size:12px
}

.upload small{
    color:#607996
}

#report{
    display:block;
    width:100%;
    margin-top:13px;
    padding:7px
}

.file-label{
    display:inline-block;
    margin-top:10px;
    padding:10px 17px;
    border:1px solid rgba(168,85,247,.45);
    border-radius:10px;
    color:#cda7ff;
    background:rgba(168,85,247,.055);
    cursor:pointer;
    font-size:12px;
    font-weight:800;
    transition:.2s
}

.file-label:hover{
    border-color:var(--violet);
    background:rgba(168,85,247,.10);
    box-shadow:0 0 25px rgba(168,85,247,.10)
}

.primary-button{
    width:100%;
    margin-top:18px;
    padding:16px 22px;
    border:1px solid rgba(37,231,255,.50);
    border-radius:13px;
    color:white;
    background:
        linear-gradient(100deg,#00bfe8,#526cff,#a63ff0);
    background-size:180% 100%;
    font-size:14px;
    font-weight:900;
    letter-spacing:.2px;
    cursor:pointer;
    box-shadow:
        0 10px 35px rgba(37,231,255,.12),
        0 10px 35px rgba(168,85,247,.12);
    transition:.25s
}

.primary-button:hover{
    transform:translateY(-2px);
    background-position:100% 0;
    box-shadow:
        0 15px 40px rgba(37,231,255,.18),
        0 15px 40px rgba(168,85,247,.18)
}

.primary-button:disabled{
    opacity:.55;
    cursor:wait;
    transform:none
}

.status{
    min-height:20px;
    margin-top:13px;
    text-align:center;
    color:var(--cyan);
    font-size:12px
}

.status.error{color:var(--red)}

.results-head{
    display:flex;
    justify-content:space-between;
    align-items:center;
    gap:15px;
    margin:32px 0 15px
}

.results-label{
    color:#7189a6;
    font-size:10px;
    font-weight:900;
    letter-spacing:1.2px
}

.results-label span{
    color:var(--cyan)
}

.table-wrap{
    overflow-x:auto;
    border:1px solid rgba(83,221,255,.14);
    border-radius:14px
}

table{
    width:100%;
    min-width:940px;
    border-collapse:collapse
}

caption{
    text-align:left;
    padding:11px;
    color:var(--muted);
    font-size:11px
}

th,td{
    padding:12px;
    border-bottom:1px solid rgba(110,180,255,.08);
    text-align:left;
    vertical-align:top;
    font-size:12px
}

th{
    background:rgba(37,231,255,.045);
    color:#94b4d4;
    font-size:9px;
    text-transform:uppercase;
    letter-spacing:.7px
}

td{color:#d8e6f5}

tr:hover td{
    background:rgba(37,231,255,.025)
}

.badge{
    display:inline-block;
    min-width:65px;
    padding:5px 9px;
    text-align:center;
    border-radius:20px;
    font-size:9px;
    font-weight:900;
    letter-spacing:.5px
}

.low{
    background:rgba(255,209,102,.10);
    color:var(--yellow);
    border:1px solid rgba(255,209,102,.20)
}

.normal{
    background:rgba(57,242,174,.09);
    color:var(--green);
    border:1px solid rgba(57,242,174,.20)
}

.high{
    background:rgba(255,85,119,.10);
    color:var(--red);
    border:1px solid rgba(255,85,119,.22)
}

.unknown{
    background:rgba(130,155,185,.08);
    color:#a5b5c8;
    border:1px solid rgba(130,155,185,.16)
}

.dashboard-grid{
    display:grid;
    grid-template-columns:1.55fr .75fr;
    gap:20px
}

.conflict{
    padding:13px;
    margin:8px 0;
    border-radius:11px;
    background:rgba(255,190,70,.055);
    border:1px solid rgba(255,190,70,.18);
    border-left:3px solid var(--yellow);
    color:#e7d8ac;
    font-size:12px;
    line-height:1.55
}

.summary{
    padding:18px;
    border-radius:13px;
    background:
        linear-gradient(135deg,rgba(37,231,255,.045),rgba(168,85,247,.06));
    border:1px solid rgba(83,221,255,.12);
    line-height:1.7;
    color:#d8e8f8;
    font-size:13px
}

.notice{
    padding:17px;
    border-radius:12px;
    background:
        linear-gradient(135deg,rgba(57,242,174,.035),rgba(37,231,255,.035));
    border:1px solid rgba(57,242,174,.13);
    border-left:3px solid var(--green);
    line-height:1.65;
    color:#c9d8e8;
    font-size:12px
}

.notice strong{
    color:var(--green)
}

.empty{
    color:#738ba5;
    padding:10px 0;
    font-size:12px
}

.metric{
    display:flex;
    justify-content:space-between;
    align-items:center;
    padding:9px 0;
    border-bottom:1px solid rgba(100,170,220,.08);
    color:#7890a9;
    font-size:11px
}

.metric strong{
    color:#dcecff
}

.footer{
    text-align:center;
    color:#4d637d;
    font-size:10px;
    padding:18px 0 38px;
    letter-spacing:.3px
}

.footer span{
    color:var(--violet)
}

.sr-only{
    position:absolute;
    width:1px;
    height:1px;
    padding:0;
    margin:-1px;
    overflow:hidden;
    clip:rect(0,0,0,0);
    white-space:nowrap;
    border:0
}

@media(max-width:850px){
    .dashboard-grid{
        grid-template-columns:1fr
    }
}

@media(max-width:700px){
    .grid{
        grid-template-columns:1fr
    }

    .full{
        grid-column:auto
    }

    .header-inner{
        align-items:flex-start
    }

    .system-status{
        display:none
    }

    .hero{
        padding-top:32px
    }

    .hero h2{
        font-size:38px
    }

    .card{
        padding:20px
    }

    .step-line{
        width:25px
    }
}
</style>
</head>

<body>

<header class="header">
<div class="header-inner">

<div class="brand">
<div class="logo" aria-hidden="true">🧬</div>

<div>
<h1><span class="cyan">Med</span><span class="violet">Lens</span></h1>
<p>AI CLINICAL INFORMATION INTELLIGENCE</p>
</div>
</div>

<div class="system-status">
<span class="status-dot" aria-hidden="true"></span>
AI SYSTEM ONLINE
</div>

</div>
</header>


<section class="hero">

<div>
<div class="hero-kicker">◈ MULTIMODAL AI · STRUCTURED CLINICAL DATA</div>

<h2>
Your reports.<br>
<span>Structured intelligence.</span>
</h2>

<p class="hero-text">
Transform medical reports into structured, reviewable information
with reference-aware extraction, conflict detection and
patient-friendly summaries — while keeping human verification
at the center.
</p>

<div class="pipeline" aria-label="MedLens processing workflow">

<div class="step">
<span class="step-number">01</span>
PATIENT
</div>

<div class="step-line"></div>

<div class="step">
<span class="step-number">02</span>
REPORT
</div>

<div class="step-line"></div>

<div class="step">
<span class="step-number">03</span>
AI EXTRACT
</div>

<div class="step-line"></div>

<div class="step">
<span class="step-number">04</span>
REVIEW
</div>

</div>
</div>

</section>


<main class="container">

<section class="card" aria-labelledby="patient-heading">

<div class="title">

<div class="icon" aria-hidden="true">👤</div>

<div>
<h3 id="patient-heading">Patient Information</h3>
<div class="sub">Optional context supplied by the user</div>
</div>

</div>


<div class="grid">

<div>
<label for="age">AGE</label>
<input
id="age"
name="age"
type="number"
min="0"
max="150"
placeholder="e.g. 21"
autocomplete="off">
</div>


<div>
<label for="sex">SEX</label>

<select id="sex" name="sex">
<option value="">Select</option>
<option>Male</option>
<option>Female</option>
<option>Other</option>
<option>Prefer not to say</option>
</select>

</div>


<div class="full">
<label for="symptoms">SYMPTOMS</label>

<textarea
id="symptoms"
name="symptoms"
placeholder="Enter patient-reported symptoms"></textarea>
</div>


<div>
<label for="conditions">KNOWN CONDITIONS</label>

<textarea
id="conditions"
name="conditions"
placeholder="Existing conditions"></textarea>
</div>


<div>
<label for="allergies">ALLERGIES</label>

<textarea
id="allergies"
name="allergies"
placeholder="Known allergies"></textarea>
</div>


<div class="full">
<label for="medications">CURRENT MEDICATIONS</label>

<textarea
id="medications"
name="medications"
placeholder="Current medications"></textarea>
</div>

</div>

</section>


<section class="card" aria-labelledby="report-heading">

<div class="title">

<div class="icon" aria-hidden="true">📄</div>

<div>
<h3 id="report-heading">Medical Report</h3>
<div class="sub">Upload a source document for multimodal AI processing</div>
</div>

</div>


<div class="upload">

<div class="upload-icon" aria-hidden="true">☁️</div>

<strong>Upload Medical Report</strong>

<p>PDF · JPG · PNG · WEBP</p>

<small id="report-help">
Maximum file size: 8 MB
</small>


<label for="report" class="file-label">
Choose medical report
</label>

<input
id="report"
name="report"
type="file"
accept=".pdf,.jpg,.jpeg,.png,.webp"
aria-describedby="report-help">

</div>


<button
id="processBtn"
class="primary-button"
type="button"
onclick="processReport()"
aria-describedby="status">

⚡ Process Medical Report

</button>


<div
id="status"
class="status"
role="status"
aria-live="polite"
aria-atomic="true">
</div>

</section>


<div id="results" aria-live="polite"></div>


<div class="footer">
<span>MedLens</span> · Clinical information structuring · Human review required
</div>

</main>


<script>

function escapeHTML(value){

if(value===null || value===undefined){
return "";
}

return String(value)
.replace(/&/g,"&amp;")
.replace(/</g,"&lt;")
.replace(/>/g,"&gt;")
.replace(/"/g,"&quot;")
.replace(/'/g,"&#039;");

}


function statusBadge(status){

const value=String(status||"UNKNOWN").toUpperCase();

let cls="unknown";

if(value==="LOW") cls="low";
if(value==="NORMAL") cls="normal";
if(value==="HIGH") cls="high";

return `
<span
class="badge ${cls}"
aria-label="Status: ${escapeHTML(value)}">
${escapeHTML(value)}
</span>`;

}


function showError(message){

const status=document.getElementById("status");

status.classList.add("error");
status.textContent="✕ "+message;

}


async function processReport(){

const fileInput=document.getElementById("report");
const button=document.getElementById("processBtn");
const status=document.getElementById("status");
const results=document.getElementById("results");

status.classList.remove("error");


if(!fileInput.files.length){

showError("Please upload a medical report first.");
fileInput.focus();
return;

}


const file=fileInput.files[0];


if(file.size>8*1024*1024){

showError("File is too large. Maximum allowed size is 8 MB.");
fileInput.focus();
return;

}


const patient={

age:document.getElementById("age").value,
sex:document.getElementById("sex").value,
symptoms:document.getElementById("symptoms").value,
conditions:document.getElementById("conditions").value,
allergies:document.getElementById("allergies").value,
medications:document.getElementById("medications").value

};


const formData=new FormData();

formData.append("file",file);
formData.append("patient",JSON.stringify(patient));


button.disabled=true;
button.setAttribute("aria-busy","true");
button.textContent="⏳ AI PROCESSING...";

status.textContent="◈ Reading and structuring the medical report...";
results.innerHTML="";


try{

const response=await fetch("/analyze",{
method:"POST",
body:formData
});


let data;

try{

data=await response.json();

}catch{

throw new Error("The server returned an unexpected response.");

}


if(data.error){

throw new Error(data.error);

}


renderResults(data);

status.classList.remove("error");
status.textContent="✓ Analysis complete — review the structured information.";


}catch(error){

showError(error.message||"Unable to process report.");


}finally{

button.disabled=false;
button.removeAttribute("aria-busy");
button.textContent="⚡ Process Medical Report";

}

}


function renderResults(data){

const results=document.getElementById("results");

let rows="";

const tests=Array.isArray(data.tests) ? data.tests : [];


if(tests.length){

tests.forEach((test,index)=>{

rows+=`

<tr>

<td>${escapeHTML(index+1)}</td>

<td>${escapeHTML(test.test_name)}</td>

<td>${escapeHTML(test.value)}</td>

<td>${escapeHTML(test.unit)}</td>

<td>${escapeHTML(test.reference_range)}</td>

<td>${statusBadge(test.status)}</td>

<td>${escapeHTML(test.date)}</td>

<td>${escapeHTML(test.observation)}</td>

<td>${escapeHTML(test.source)}</td>

</tr>`;

});

}else{

rows=`

<tr>

<td colspan="9" class="empty">
No structured test results were extracted.
</td>

</tr>`;

}


let conflicts="";

const conflictList=
Array.isArray(data.conflicts) ? data.conflicts : [];


if(conflictList.length){

conflictList.forEach(item=>{

conflicts+=`

<div class="conflict" role="alert">
⚠️ ${escapeHTML(item)}
</div>`;

});

}else{

conflicts=`

<p class="empty">
✓ No conflicts were detected in the supplied information.
</p>`;

}


results.innerHTML=`

<div class="results-head">

<div class="results-label">
ANALYSIS <span>COMPLETE</span>
</div>

<div class="results-label">
${tests.length} TESTS EXTRACTED
</div>

</div>


<section class="card" aria-labelledby="record-heading">

<div class="title">

<div class="icon" aria-hidden="true">📊</div>

<div>
<h3 id="record-heading">Structured Medical Record</h3>
<div class="sub">
AI-extracted information from the uploaded source
</div>
</div>

</div>


<div class="table-wrap">

<table>

<caption>
Structured medical test results extracted from the uploaded report
</caption>

<thead>

<tr>

<th scope="col">#</th>
<th scope="col">Test</th>
<th scope="col">Value</th>
<th scope="col">Unit</th>
<th scope="col">Reference Range</th>
<th scope="col">Status</th>
<th scope="col">Date</th>
<th scope="col">Observation</th>
<th scope="col">Source</th>

</tr>

</thead>

<tbody>
${rows}
</tbody>

</table>

</div>

</section>


<div class="dashboard-grid">


<section class="card" aria-labelledby="summary-heading">

<div class="title">

<div class="icon" aria-hidden="true">🧠</div>

<div>
<h3 id="summary-heading">Patient-Friendly Summary</h3>
<div class="sub">Simplified information found in the report</div>
</div>

</div>


<div class="summary">
${escapeHTML(data.summary||"No summary generated.")}
</div>

</section>


<section class="card" aria-labelledby="conflict-heading">

<div class="title">

<div class="icon" aria-hidden="true">⚠️</div>

<div>
<h3 id="conflict-heading">Conflict Detection</h3>
<div class="sub">Potential inconsistencies requiring review</div>
</div>

</div>

${conflicts}

</section>

</div>


<section class="card" aria-labelledby="responsible-heading">

<div class="title">

<div class="icon" aria-hidden="true">🛡️</div>

<div>
<h3 id="responsible-heading">Responsible AI</h3>
<div class="sub">Safety and transparency layer</div>
</div>

</div>


<div class="notice">

<strong>MedLens is a review-support tool.</strong>

<br><br>

It does not provide medical diagnosis, prescribe treatment,
recommend medication changes, or determine medication dosage.

<br><br>

Reference-range status is marked LOW, NORMAL, or HIGH only
when the uploaded report provides a usable reference range.
Otherwise, the status is shown as UNKNOWN.

<br><br>

AI-extracted information should be reviewed by a qualified
human against the original report before clinical use.

</div>

</section>

`;

}

</script>

</body>
</html>
"""


@app.get("/", response_class=HTMLResponse)
async def home():
    return HTML


def clean_json_text(text):
    text = str(text or "").strip()

    text = re.sub(
        r"^```json\s*",
        "",
        text,
        flags=re.IGNORECASE
    )

    text = re.sub(
        r"^```\s*",
        "",
        text
    )

    text = re.sub(
        r"\s*```$",
        "",
        text
    )

    start = text.find("{")
    end = text.rfind("}")

    if start != -1 and end != -1 and end > start:
        text = text[start:end + 1]

    return text.strip()


def make_data_url(file_bytes, mime_type):
    encoded = base64.b64encode(file_bytes).decode("utf-8")
    return f"data:{mime_type};base64,{encoded}"


def _first_number(value):
    """
    Extract the first numeric value from a field.
    This deliberately uses the first number because some reports
    contain values such as '1.0-2.0*' where the report may have
    scanned a range-like value into the value column.
    """
    if value is None:
        return None

    text = str(value).replace(",", "")

    match = re.search(
        r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)",
        text
    )

    if not match:
        return None

    try:
        return float(match.group(0))
    except ValueError:
        return None


def _numbers(value):
    if value is None:
        return []

    text = str(value).replace(",", "")

    found = re.findall(
        r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)",
        text
    )

    numbers = []

    for item in found:
        try:
            numbers.append(float(item))
        except ValueError:
            pass

    return numbers


def classify_from_reference(value, reference):
    """
    Classify a result only when the source report provides
    a reference range or reference value.

    Supports common report formats such as:
      5.0-8.0
      5.0–8.0
      <140
      <=140
      >5
      >=5
      Negative
      None
      Occasional

    If the source reference cannot be interpreted safely,
    UNKNOWN is returned.
    """

    value_text = str(value or "").strip()
    ref_text = str(reference or "").strip()

    if not value_text or not ref_text:
        return "UNKNOWN"

    value_lower = value_text.lower().strip()
    ref_lower = ref_text.lower().strip()

    # Remove common report markers without changing meaning.
    value_clean = value_lower.replace("*", "").strip()
    ref_clean = ref_lower.replace("*", "").strip()

    # Exact qualitative references.
    qualitative_normal = {
        "negative",
        "none",
        "absent",
        "not detected",
        "not seen",
        "nil",
        "normal",
        "clear",
        "occasional"
    }

    if ref_clean in qualitative_normal:
        if value_clean == ref_clean:
            return "NORMAL"

        # Common report convention:
        # if a reference explicitly says Negative/None/etc.,
        # a different reported finding is outside that reference.
        return "HIGH"

    # Handle strict upper bounds: <140, <=140.
    upper_match = re.fullmatch(
        r"(?:less than|<|<=)\s*([-+]?(?:\d+(?:\.\d*)?|\.\d+))",
        ref_clean
    )

    if upper_match:
        ref_value = float(upper_match.group(1))
        actual = _first_number(value_clean)

        if actual is None:
            return "UNKNOWN"

        if "<=" in ref_clean or "less than or equal" in ref_clean:
            return "NORMAL" if actual <= ref_value else "HIGH"

        return "NORMAL" if actual < ref_value else "HIGH"

    # Handle strict lower bounds: >5, >=5.
    lower_match = re.fullmatch(
        r"(?:greater than|>|>=)\s*([-+]?(?:\d+(?:\.\d*)?|\.\d+))",
        ref_clean
    )

    if lower_match:
        ref_value = float(lower_match.group(1))
        actual = _first_number(value_clean)

        if actual is None:
            return "UNKNOWN"

        if ">=" in ref_clean or "greater than or equal" in ref_clean:
            return "NORMAL" if actual >= ref_value else "LOW"

        return "NORMAL" if actual > ref_value else "LOW"

    # Extract numeric reference boundaries.
    ref_numbers = _numbers(ref_clean)

    if len(ref_numbers) >= 2:
        low = ref_numbers[0]
        high = ref_numbers[1]

        if low > high:
            low, high = high, low

        actual = _first_number(value_clean)

        if actual is None:
            return "UNKNOWN"

        if actual < low:
            return "LOW"

        if actual > high:
            return "HIGH"

        return "NORMAL"

    # A single numeric reference is not enough to determine
    # LOW/NORMAL/HIGH safely.
    return "UNKNOWN"


def normalize_result(data):
    if not isinstance(data, dict):
        data = {}

    tests = data.get("tests", [])

    if not isinstance(tests, list):
        tests = []

    normalized_tests = []

    for test in tests:

        if not isinstance(test, dict):
            continue

        test_name = str(
            test.get("test_name", "")
        ).strip()

        value = str(
            test.get("value", "")
        ).strip()

        unit = str(
            test.get("unit", "")
        ).strip()

        reference_range = str(
            test.get("reference_range", "")
        ).strip()

        date = str(
            test.get("date", "")
        ).strip()

        observation = str(
            test.get("observation", "")
        ).strip()

        source = str(
            test.get("source", "uploaded report")
        ).strip()

        ai_status = str(
            test.get("status", "UNKNOWN")
        ).upper().strip()

        if ai_status not in [
            "LOW",
            "NORMAL",
            "HIGH",
            "UNKNOWN"
        ]:
            ai_status = "UNKNOWN"

        # Critical reliability layer:
        # whenever a reference range exists, calculate the
        # classification ourselves from that source reference.
        #
        # This prevents the model from returning UNKNOWN when
        # a directly comparable source range is available.
        calculated_status = classify_from_reference(
            value,
            reference_range
        )

        if calculated_status != "UNKNOWN":
            status = calculated_status
        else:
            status = ai_status

        # If no reference exists, never allow the AI to invent
        # LOW/NORMAL/HIGH. The safe result is UNKNOWN.
        if not reference_range:
            status = "UNKNOWN"

        normalized_tests.append({

            "test_name": test_name,

            "value": value,

            "unit": unit,

            "reference_range": reference_range,

            "status": status,

            "date": date,

            "observation": observation,

            "source": source or "uploaded report"

        })


    conflicts = data.get("conflicts", [])

    if not isinstance(conflicts, list):
        conflicts = [str(conflicts)]


    return {

        "tests": normalized_tests,

        "conflicts": [
            str(x)
            for x in conflicts
        ],

        "summary": str(
            data.get("summary", "")
        )

    }


@app.post("/analyze")
async def analyze(
    file: UploadFile = File(...),
    patient: str = Form("{}")
):

    api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:

        return {
            "error":
            "OPENROUTER_API_KEY is not configured in Render."
        }


    allowed_types = {
        "application/pdf",
        "image/jpeg",
        "image/png",
        "image/webp"
    }


    mime_type = (
        file.content_type
        or "application/octet-stream"
    )


    if mime_type not in allowed_types:

        return {
            "error":
            "Unsupported file type. Please upload PDF, JPG, PNG, or WEBP."
        }


    file_bytes = await file.read()


    if len(file_bytes) > 8 * 1024 * 1024:

        return {
            "error":
            "File is too large. Maximum allowed size is 8 MB."
        }


    try:

        patient_data = json.loads(patient)

        if not isinstance(patient_data, dict):
            patient_data = {}

    except Exception:

        patient_data = {}


    # Limit user-provided text so unnecessarily large prompts
    # are not sent to the AI service.
    for key in list(patient_data.keys()):

        value = patient_data[key]

        if isinstance(value, str):

            patient_data[key] = value[:1000]


    prompt = f"""
You are the extraction engine for MedLens,
a clinical information structuring application.

Your task is ONLY to read the uploaded medical report
and convert its information into structured data.

PATIENT-PROVIDED INFORMATION:
{json.dumps(patient_data, ensure_ascii=False)}

STRICT SAFETY AND ACCURACY RULES:

1. Extract medical test information ONLY from the uploaded report.
2. NEVER invent a laboratory value.
3. NEVER invent a unit.
4. NEVER invent a date.
5. NEVER invent a reference range.
6. Preserve the reference range exactly as it appears in the report.
7. LOW, NORMAL, or HIGH may ONLY be assigned using a
   reference range explicitly present in the uploaded report.
8. If a usable reference range exists, compare the reported
   value directly against that source range.
9. For numeric ranges:
   - below the lower bound = LOW
   - inside the range = NORMAL
   - above the upper bound = HIGH
10. For references such as "<140":
    values below the stated upper limit are NORMAL;
    values at or above the limit are HIGH.
11. For references such as ">5":
    values above the stated lower limit are NORMAL;
    values at or below the limit are LOW.
12. For qualitative references such as Negative, None,
    Absent or similar, preserve the exact source wording.
13. If a reference range cannot safely support a comparison,
    use UNKNOWN.
14. Do not use general medical knowledge to create ranges.
15. Do not diagnose, infer, or speculate about disease.
16. If the report mentions a diagnosis or interpretation,
    reproduce it only as an attributed statement such as
    "The report states..." or "The report mentions...".
17. Do not turn observations into medical conclusions.
18. Do not recommend treatment or medication changes.
19. Do not recommend dosage changes.
20. Do not present uncertain information as fact.
21. Detect obvious contradictions between supplied patient
    information and the uploaded report.
22. Missing optional patient information is not a conflict.
23. Keep the summary concise, factual, and patient-friendly.
24. Preserve source information and dates when readable.
25. Do not add information that is not present in the source.

Return ONLY valid JSON.

Use exactly:

{{
  "tests": [
    {{
      "test_name": "string",
      "value": "string",
      "unit": "string",
      "reference_range": "string",
      "status": "LOW | NORMAL | HIGH | UNKNOWN",
      "date": "string",
      "observation": "string",
      "source": "uploaded report"
    }}
  ],
  "conflicts": ["string"],
  "summary": "string"
}}

Do not wrap JSON in markdown.
"""


    data_url = make_data_url(
        file_bytes,
        mime_type
    )


    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }


    if mime_type == "application/pdf":

        content = [

            {
                "type": "text",
                "text": prompt
            },

            {
                "type": "file",
                "file": {
                    "filename":
                    file.filename or "medical_report.pdf",

                    "file_data":
                    data_url
                }
            }

        ]

    else:

        content = [

            {
                "type": "text",
                "text": prompt
            },

            {
                "type": "image_url",
                "image_url": {
                    "url": data_url
                }
            }

        ]


    payload = {

        "model":
        "minimax/minimax-m3:free",

        "messages": [

            {
                "role": "user",
                "content": content
            }

        ],

        "temperature": 0.1,

        "max_tokens": 2500

    }


    try:

        response = requests.post(

            "https://openrouter.ai/api/v1/chat/completions",

            headers=headers,

            json=payload,

            timeout=90

        )


        if not response.ok:

            return {

                "error":
                (
                    f"OpenRouter API error "
                    f"{response.status_code}: "
                    f"{response.text[:1000]}"
                )

            }


        result = response.json()

        choices = result.get("choices", [])


        if not choices:

            return {
                "error":
                "OpenRouter returned no model response."
            }


        message = choices[0].get(
            "message",
            {}
        )


        content = message.get(
            "content",
            ""
        )


        if isinstance(content, list):

            parts = []

            for item in content:

                if (
                    isinstance(item, dict)
                    and "text" in item
                ):

                    parts.append(
                        str(item["text"])
                    )

                else:

                    parts.append(
                        str(item)
                    )

            content = "".join(parts)


        content = str(content)

        cleaned = clean_json_text(content)


        try:

            parsed = json.loads(cleaned)

        except Exception:

            return {

                "error":
                (
                    "The AI returned an unexpected format. "
                    f"Raw response: {content[:1000]}"
                )

            }


        return normalize_result(parsed)


    except requests.exceptions.Timeout:

        return {
            "error":
            "OpenRouter request timed out. Please try again."
        }


    except requests.exceptions.RequestException as e:

        return {

            "error":
            (
                "Network error while contacting OpenRouter: "
                f"{str(e)[:300]}"
            )

        }


    except Exception as e:

        return {

            "error":
            (
                "AI processing failed: "
                f"{type(e).__name__}: "
                f"{str(e)[:300]}"
            )

        }
