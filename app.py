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
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="MedLens AI clinical information structuring tool">
<title>MedLens — Clinical Intelligence</title>

<style>
*{box-sizing:border-box}

:root{
 --bg:#040405;
 --surface:#0b0b0f;
 --surface2:#111117;
 --surface3:#17171e;
 --text:#f5f5f7;
 --muted:#898994;
 --dim:#555560;
 --lime:#c8ff00;
 --pink:#ff2bd6;
 --violet:#985cff;
 --yellow:#ffb800;
 --red:#ff416d;
 --green:#c8ff00;
}

html,body{
 margin:0;
 min-height:100%;
}

body{
 color:var(--text);
 font-family:Inter,"Segoe UI",Arial,sans-serif;
 background:
 radial-gradient(circle at 10% 5%,rgba(200,255,0,.075),transparent 24%),
 radial-gradient(circle at 90% 8%,rgba(255,43,214,.09),transparent 25%),
 radial-gradient(circle at 50% 100%,rgba(152,92,255,.09),transparent 35%),
 var(--bg);
 overflow-x:hidden;
}

body:before{
 content:"";
 position:fixed;
 inset:0;
 pointer-events:none;
 background-image:
 linear-gradient(rgba(200,255,0,.018) 1px,transparent 1px),
 linear-gradient(90deg,rgba(255,43,214,.016) 1px,transparent 1px);
 background-size:42px 42px;
}

body:after{
 content:"";
 position:fixed;
 width:500px;
 height:500px;
 right:-250px;
 top:35%;
 border:1px solid rgba(200,255,0,.05);
 border-radius:50%;
 box-shadow:0 0 100px rgba(200,255,0,.035);
 pointer-events:none;
}

button,input,textarea,select{
 font-family:inherit;
}

button{
 cursor:pointer;
}

.app{
 position:relative;
 z-index:1;
 min-height:100vh;
}

/* HEADER */

.header{
 height:76px;
 display:flex;
 align-items:center;
 justify-content:space-between;
 padding:0 30px;
 border-bottom:1px solid rgba(255,255,255,.07);
 background:rgba(4,4,5,.86);
 backdrop-filter:blur(20px);
}

.brand{
 display:flex;
 align-items:center;
 gap:12px;
}

.logo{
 width:42px;
 height:42px;
 display:grid;
 place-items:center;
 border-radius:13px;
 background:linear-gradient(135deg,rgba(200,255,0,.12),rgba(255,43,214,.14));
 border:1px solid rgba(200,255,0,.35);
 box-shadow:0 0 25px rgba(200,255,0,.08);
}

.brand-name{
 font-size:21px;
 font-weight:900;
 letter-spacing:-.8px;
}

.brand-name .lime{color:var(--lime)}
.brand-name .pink{color:var(--pink)}

.brand-sub{
 margin-top:2px;
 color:#666670;
 font-size:8px;
 letter-spacing:1.2px;
}

.system{
 display:flex;
 align-items:center;
 gap:8px;
 color:var(--lime);
 font-size:8px;
 font-weight:900;
 letter-spacing:1px;
}

.system-dot{
 width:7px;
 height:7px;
 border-radius:50%;
 background:var(--lime);
 box-shadow:0 0 14px var(--lime);
}

/* PROGRESS */

.progress-area{
 max-width:1080px;
 margin:0 auto;
 padding:22px 24px 5px;
}

.progress{
 display:flex;
 align-items:center;
 justify-content:center;
}

.progress-step{
 display:flex;
 align-items:center;
 gap:8px;
 color:#55555e;
 font-size:8px;
 font-weight:900;
 letter-spacing:.8px;
 transition:.3s;
}

.progress-step.active{
 color:var(--lime);
}

.progress-step.done{
 color:#9999a4;
}

.progress-number{
 width:25px;
 height:25px;
 display:grid;
 place-items:center;
 border-radius:50%;
 border:1px solid #34343b;
 background:#0a0a0d;
 font-size:8px;
}

.progress-step.active .progress-number{
 color:#050505;
 background:var(--lime);
 border-color:var(--lime);
 box-shadow:0 0 18px rgba(200,255,0,.25);
}

.progress-step.done .progress-number{
 border-color:rgba(200,255,0,.35);
 color:var(--lime);
}

.progress-line{
 width:55px;
 height:1px;
 margin:0 8px;
 background:#292930;
}

.progress-line.done{
 background:linear-gradient(90deg,var(--lime),var(--pink));
}

/* SCREENS */

.screen{
 display:none;
 max-width:1080px;
 margin:0 auto;
 padding:50px 24px 40px;
 animation:screenIn .45s ease;
}

.screen.active{
 display:block;
}

@keyframes screenIn{
 from{
  opacity:0;
  transform:translateX(25px);
 }
 to{
  opacity:1;
  transform:translateX(0);
 }
}

/* WELCOME */

.welcome{
 min-height:calc(100vh - 130px);
 display:flex;
 align-items:center;
 justify-content:center;
 text-align:center;
}

.welcome-inner{
 max-width:800px;
}

.kicker{
 display:inline-block;
 padding:8px 13px;
 border:1px solid rgba(255,43,214,.32);
 border-radius:30px;
 color:#ff65e2;
 background:rgba(255,43,214,.045);
 font-size:8px;
 font-weight:900;
 letter-spacing:1.4px;
}

.welcome h1{
 margin:22px 0 15px;
 font-size:clamp(48px,8vw,88px);
 line-height:.92;
 letter-spacing:-5px;
}

.gradient{
 background:linear-gradient(90deg,var(--lime),var(--pink),var(--violet));
 -webkit-background-clip:text;
 background-clip:text;
 color:transparent;
}

.welcome-text{
 max-width:650px;
 margin:auto;
 color:var(--muted);
 line-height:1.8;
 font-size:14px;
}

.start-btn{
 margin-top:30px;
 padding:16px 34px;
 border:1px solid rgba(200,255,0,.55);
 border-radius:12px;
 background:linear-gradient(100deg,var(--lime),#e4ff70,var(--pink));
 color:#050505;
 font-size:11px;
 font-weight:950;
 letter-spacing:.8px;
 box-shadow:0 12px 40px rgba(200,255,0,.12);
 transition:.25s;
}

.start-btn:hover{
 transform:translateY(-3px);
 box-shadow:0 18px 50px rgba(255,43,214,.15);
}

.welcome-grid{
 display:grid;
 grid-template-columns:repeat(3,1fr);
 gap:12px;
 margin-top:55px;
}

.feature{
 padding:18px;
 border:1px solid rgba(255,255,255,.07);
 border-radius:14px;
 background:rgba(12,12,16,.65);
 text-align:left;
}

.feature-icon{
 font-size:18px;
 margin-bottom:10px;
}

.feature strong{
 display:block;
 font-size:10px;
 margin-bottom:5px;
}

.feature span{
 color:#686873;
 font-size:9px;
 line-height:1.5;
}

/* CARDS */

.card{
 position:relative;
 overflow:hidden;
 padding:27px;
 border-radius:20px;
 border:1px solid rgba(200,255,0,.13);
 background:linear-gradient(145deg,rgba(16,16,21,.96),rgba(7,7,9,.96));
 box-shadow:0 25px 75px rgba(0,0,0,.58);
}

.card:before{
 content:"";
 position:absolute;
 top:0;
 left:25px;
 right:25px;
 height:1px;
 background:linear-gradient(90deg,transparent,var(--lime),var(--pink),transparent);
 opacity:.7;
}

.page-title{
 margin-bottom:25px;
}

.page-title small{
 color:var(--lime);
 font-size:8px;
 font-weight:900;
 letter-spacing:1.5px;
}

.page-title h2{
 margin:8px 0 6px;
 font-size:32px;
 letter-spacing:-1.5px;
}

.page-title p{
 margin:0;
 color:var(--muted);
 font-size:12px;
}

.grid{
 display:grid;
 grid-template-columns:repeat(2,1fr);
 gap:15px;
}

.full{
 grid-column:1/-1;
}

label{
 display:block;
 margin-bottom:7px;
 color:#aaaab4;
 font-size:9px;
 font-weight:900;
 letter-spacing:.8px;
}

input,textarea,select{
 width:100%;
 padding:13px;
 color:var(--text);
 background:#08080a;
 border:1px solid rgba(255,255,255,.09);
 border-radius:11px;
 outline:none;
 font-size:12px;
}

input::placeholder,
textarea::placeholder{
 color:#50505a;
}

input:focus,
textarea:focus,
select:focus{
 border-color:rgba(200,255,0,.65);
 box-shadow:0 0 0 3px rgba(200,255,0,.045);
}

input:focus-visible,
textarea:focus-visible,
select:focus-visible,
button:focus-visible,
.file-label:focus-visible{
 outline:2px solid var(--lime);
 outline-offset:3px;
}

textarea{
 min-height:82px;
 resize:vertical;
}

select option{
 background:#111116;
}

.next-row{
 display:flex;
 justify-content:space-between;
 align-items:center;
 gap:12px;
 margin-top:20px;
}

.back-btn{
 padding:13px 20px;
 border-radius:10px;
 border:1px solid rgba(255,255,255,.1);
 color:#aaaab2;
 background:#0b0b0f;
 font-size:10px;
 font-weight:900;
}

.back-btn:hover{
 border-color:rgba(255,255,255,.22);
 color:white;
}

.next-btn{
 padding:14px 24px;
 border:1px solid rgba(200,255,0,.45);
 border-radius:10px;
 color:#050505;
 background:var(--lime);
 font-size:10px;
 font-weight:950;
 letter-spacing:.5px;
}

.next-btn:hover{
 box-shadow:0 0 30px rgba(200,255,0,.14);
 transform:translateY(-1px);
}

/* UPLOAD */

.upload-zone{
 padding:55px 20px;
 text-align:center;
 border:1px dashed rgba(200,255,0,.4);
 border-radius:18px;
 background:
 radial-gradient(circle at 50% 20%,rgba(200,255,0,.06),transparent 45%),
 rgba(4,4,7,.7);
 transition:.25s;
}

.upload-zone.drag{
 border-color:var(--pink);
 background:rgba(255,43,214,.04);
}

.upload-icon{
 width:70px;
 height:70px;
 margin:auto auto 15px;
 display:grid;
 place-items:center;
 border-radius:21px;
 background:linear-gradient(135deg,rgba(200,255,0,.1),rgba(255,43,214,.11));
 border:1px solid rgba(200,255,0,.22);
 font-size:29px;
}

.upload-zone strong{
 display:block;
 font-size:15px;
}

.upload-zone p{
 color:var(--muted);
 font-size:11px;
}

.file-label{
 display:inline-block;
 padding:11px 18px;
 border-radius:10px;
 border:1px solid rgba(255,43,214,.4);
 color:#ff65e2;
 background:rgba(255,43,214,.04);
 cursor:pointer;
 font-size:10px;
 font-weight:900;
}

.file-label:hover{
 border-color:var(--pink);
 box-shadow:0 0 25px rgba(255,43,214,.1);
}

#report{
 display:none;
}

.file-info{
 display:none;
 margin-top:18px;
 padding:12px;
 border-radius:10px;
 border:1px solid rgba(200,255,0,.15);
 color:var(--lime);
 background:rgba(200,255,0,.035);
 font-size:10px;
}

/* PROCESSING */

.processing{
 min-height:65vh;
 display:flex;
 align-items:center;
 justify-content:center;
 text-align:center;
}

.processing-inner{
 width:100%;
 max-width:620px;
}

.orb{
 width:105px;
 height:105px;
 margin:0 auto 30px;
 border-radius:50%;
 border:1px solid rgba(200,255,0,.4);
 background:
 radial-gradient(circle,rgba(200,255,0,.15),transparent 58%);
 box-shadow:
 0 0 35px rgba(200,255,0,.12),
 inset 0 0 35px rgba(255,43,214,.08);
 display:grid;
 place-items:center;
 font-size:36px;
 animation:pulse 1.8s infinite;
}

@keyframes pulse{
 0%,100%{transform:scale(1);box-shadow:0 0 30px rgba(200,255,0,.1)}
 50%{transform:scale(1.07);box-shadow:0 0 60px rgba(255,43,214,.16)}
}

.processing h2{
 margin:0 0 8px;
 font-size:27px;
}

.processing p{
 color:var(--muted);
 font-size:11px;
}

.processing-steps{
 margin-top:30px;
 display:grid;
 gap:8px;
}

.processing-step{
 display:flex;
 align-items:center;
 gap:12px;
 padding:12px 15px;
 border:1px solid rgba(255,255,255,.06);
 border-radius:10px;
 color:#55555f;
 background:rgba(10,10,13,.7);
 text-align:left;
 font-size:10px;
 font-weight:900;
}

.processing-step.active{
 color:var(--lime);
 border-color:rgba(200,255,0,.2);
}

.processing-step.done{
 color:#8d8d97;
}

.processing-step .mark{
 margin-left:auto;
}

/* RESULTS */

.results-header{
 display:flex;
 justify-content:space-between;
 align-items:end;
 margin-bottom:18px;
}

.results-header h2{
 margin:6px 0 0;
 font-size:29px;
 letter-spacing:-1.2px;
}

.results-count{
 color:var(--lime);
 font-size:9px;
 font-weight:900;
}

.table-wrap{
 overflow-x:auto;
 border:1px solid rgba(200,255,0,.11);
 border-radius:13px;
}

table{
 width:100%;
 min-width:960px;
 border-collapse:collapse;
}

caption{
 text-align:left;
 padding:10px;
 color:var(--muted);
 font-size:9px;
}

th,td{
 padding:11px;
 text-align:left;
 vertical-align:top;
 border-bottom:1px solid rgba(255,255,255,.055);
 font-size:10px;
}

th{
 color:#b6d679;
 background:rgba(200,255,0,.03);
 font-size:8px;
 text-transform:uppercase;
 letter-spacing:.6px;
}

td{color:#d7d7df}

tr:hover td{
 background:rgba(200,255,0,.015);
}

.badge{
 display:inline-block;
 min-width:60px;
 padding:5px 8px;
 text-align:center;
 border-radius:20px;
 font-size:8px;
 font-weight:900;
}

.normal{
 color:var(--lime);
 background:rgba(200,255,0,.07);
 border:1px solid rgba(200,255,0,.22);
}

.low{
 color:var(--yellow);
 background:rgba(255,184,0,.07);
 border:1px solid rgba(255,184,0,.2);
}

.high{
 color:#ff5278;
 background:rgba(255,65,109,.07);
 border:1px solid rgba(255,65,109,.2);
}

.unknown{
 color:#aaaab3;
 background:rgba(150,150,160,.05);
 border:1px solid rgba(150,150,160,.13);
}

.dashboard{
 display:grid;
 grid-template-columns:1.4fr .8fr;
 gap:18px;
 margin-top:18px;
}

.summary{
 padding:18px;
 border-radius:12px;
 background:linear-gradient(135deg,rgba(200,255,0,.035),rgba(255,43,214,.04));
 border:1px solid rgba(200,255,0,.11);
 color:#d7d7df;
 line-height:1.7;
 font-size:11px;
}

.conflict{
 padding:12px;
 margin:7px 0;
 border-radius:9px;
 border-left:3px solid var(--yellow);
 border-top:1px solid rgba(255,184,0,.13);
 border-right:1px solid rgba(255,184,0,.13);
 border-bottom:1px solid rgba(255,184,0,.13);
 background:rgba(255,184,0,.04);
 color:#ddd0a8;
 font-size:10px;
 line-height:1.55;
}

.notice{
 padding:16px;
 border-radius:11px;
 border:1px solid rgba(200,255,0,.12);
 border-left:3px solid var(--lime);
 background:linear-gradient(135deg,rgba(200,255,0,.03),rgba(152,92,255,.035));
 color:#c8c8d0;
 line-height:1.65;
 font-size:10px;
 margin-top:18px;
}

.notice strong{color:var(--lime)}

.result-title{
 color:#666670;
 font-size:8px;
 font-weight:900;
 letter-spacing:1px;
 margin-bottom:10px;
}

.empty{
 color:#686873;
 padding:10px 0;
 font-size:10px;
}

.footer{
 text-align:center;
 padding:20px 0 35px;
 color:#46464f;
 font-size:8px;
}

.footer span{color:var(--pink)}

/* RESPONSIVE */

@media(max-width:760px){

 .header{
  padding:0 18px;
 }

 .system{
  display:none;
 }

 .progress-area{
  padding-left:10px;
  padding-right:10px;
 }

 .progress-line{
  width:20px;
  margin:0 4px;
 }

 .progress-step{
  font-size:0;
 }

 .screen{
  padding:35px 16px;
 }

 .welcome h1{
  letter-spacing:-3px;
 }

 .welcome-grid{
  grid-template-columns:1fr;
 }

 .grid{
  grid-template-columns:1fr;
 }

 .full{
  grid-column:auto;
 }

 .dashboard{
  grid-template-columns:1fr;
 }

 .next-row{
  flex-direction:column-reverse;
 }

 .next-row button{
  width:100%;
 }

}
</style>
</head>


<body>

<div class="app">

<header class="header">

<div class="brand">

<div class="logo" aria-hidden="true">🧬</div>

<div>
<div class="brand-name">
<span class="lime">Med</span><span class="pink">Lens</span>
</div>

<div class="brand-sub">
AI CLINICAL INFORMATION INTELLIGENCE
</div>
</div>

</div>

<div class="system">
<span class="system-dot"></span>
SYSTEM ONLINE
</div>

</header>


<div class="progress-area">

<div class="progress" id="progress">

<div class="progress-step active" data-step="0">
<span class="progress-number">01</span>
WELCOME
</div>

<div class="progress-line"></div>

<div class="progress-step" data-step="1">
<span class="progress-number">02</span>
PATIENT
</div>

<div class="progress-line"></div>

<div class="progress-step" data-step="2">
<span class="progress-number">03</span>
REPORT
</div>

<div class="progress-line"></div>

<div class="progress-step" data-step="3">
<span class="progress-number">04</span>
AI
</div>

<div class="progress-line"></div>

<div class="progress-step" data-step="4">
<span class="progress-number">05</span>
RECORD
</div>

<div class="progress-line"></div>

<div class="progress-step" data-step="5">
<span class="progress-number">06</span>
INSIGHTS
</div>

</div>

</div>


<!-- SCREEN 0 -->

<section class="screen active welcome" id="screen0">

<div class="welcome-inner">

<div class="kicker">
◈ MULTIMODAL AI · CLINICAL INFORMATION STRUCTURING
</div>

<h1>
Medical data.<br>
<span class="gradient">Made intelligent.</span>
</h1>

<p class="welcome-text">
MedLens transforms scattered medical reports into structured,
reviewable information using multimodal AI, source-aware
reference classification, conflict detection and
patient-friendly summaries.
</p>

<button class="start-btn" onclick="goTo(1)">
START ANALYSIS&nbsp;&nbsp; →
</button>


<div class="welcome-grid">

<div class="feature">
<div class="feature-icon">🧬</div>
<strong>STRUCTURE</strong>
<span>Convert medical reports into organized clinical records.</span>
</div>

<div class="feature">
<div class="feature-icon">◈</div>
<strong>VALIDATE</strong>
<span>Compare results only against reference information in the source.</span>
</div>

<div class="feature">
<div class="feature-icon">🛡️</div>
<strong>RESPONSIBLE AI</strong>
<span>Review-support only. No diagnosis or treatment decisions.</span>
</div>

</div>

</div>

</section>


<!-- SCREEN 1 -->

<section class="screen" id="screen1">

<div class="page-title">
<small>STEP 01 / PATIENT CONTEXT</small>
<h2>Patient Information</h2>
<p>Provide whatever patient context is available.</p>
</div>


<div class="card">

<div class="grid">

<div>
<label for="age">AGE</label>
<input id="age" type="number" min="0" max="150"
placeholder="e.g. 21" autocomplete="off">
</div>


<div>
<label for="sex">SEX</label>

<select id="sex">
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
placeholder="Enter patient-reported symptoms"></textarea>
</div>


<div>
<label for="conditions">KNOWN CONDITIONS</label>

<textarea
id="conditions"
placeholder="Existing conditions"></textarea>
</div>


<div>
<label for="allergies">ALLERGIES</label>

<textarea
id="allergies"
placeholder="Known allergies"></textarea>
</div>


<div class="full">
<label for="medications">CURRENT MEDICATIONS</label>

<textarea
id="medications"
placeholder="Current medications"></textarea>
</div>

</div>


<div class="next-row">

<button class="back-btn" onclick="goTo(0)">
← BACK
</button>

<button class="next-btn" onclick="goTo(2)">
CONTINUE TO REPORT →
</button>

</div>

</div>

</section>


<!-- SCREEN 2 -->

<section class="screen" id="screen2">

<div class="page-title">
<small>STEP 02 / SOURCE DOCUMENT</small>
<h2>Upload Medical Report</h2>
<p>Give MedLens the original report to structure.</p>
</div>


<div class="card">

<div
class="upload-zone"
id="uploadZone"
>

<div class="upload-icon" aria-hidden="true">
☁️
</div>

<strong>Drop your medical report here</strong>

<p>
PDF · JPG · PNG · WEBP · Maximum 8 MB
</p>


<label for="report" class="file-label">
CHOOSE REPORT
</label>

<input
id="report"
type="file"
accept=".pdf,.jpg,.jpeg,.png,.webp"
>


<div id="fileInfo" class="file-info"></div>

</div>


<div class="next-row">

<button class="back-btn" onclick="goTo(1)">
← BACK
</button>

<button class="next-btn" id="analyzeBtn" onclick="startAnalysis()">
ANALYZE REPORT →
</button>

</div>

<div
id="status"
class="status"
role="status"
aria-live="polite">
</div>

</div>

</section>


<!-- SCREEN 3 -->

<section class="screen processing" id="screen3">

<div class="processing-inner">

<div class="orb" aria-hidden="true">🧠</div>

<h2>MedLens is thinking.</h2>

<p id="processingText">
Initializing clinical information pipeline...
</p>


<div class="processing-steps">

<div class="processing-step" id="p1">
<span>01</span>
READ SOURCE DOCUMENT
<span class="mark">○</span>
</div>

<div class="processing-step" id="p2">
<span>02</span>
EXTRACT CLINICAL VALUES
<span class="mark">○</span>
</div>

<div class="processing-step" id="p3">
<span>03</span>
VALIDATE REFERENCE RANGES
<span class="mark">○</span>
</div>

<div class="processing-step" id="p4">
<span>04</span>
STRUCTURE MEDICAL RECORD
<span class="mark">○</span>
</div>

</div>

</div>

</section>


<!-- SCREEN 4 -->

<section class="screen" id="screen4">

<div class="results-header">

<div>
<div class="result-title">STEP 04 / STRUCTURED DATA</div>
<h2>Clinical Record</h2>
</div>

<div class="results-count" id="testCount">
0 TESTS
</div>

</div>


<div class="card">

<div class="table-wrap">

<table>

<caption>
AI-extracted information from the uploaded source report
</caption>

<thead>

<tr>
<th scope="col">#</th>
<th scope="col">Test</th>
<th scope="col">Value</th>
<th scope="col">Unit</th>
<th scope="col">Reference</th>
<th scope="col">Status</th>
<th scope="col">Date</th>
<th scope="col">Observation</th>
<th scope="col">Source</th>
</tr>

</thead>

<tbody id="testRows"></tbody>

</table>

</div>

<div class="next-row">

<button class="back-btn" onclick="goTo(2)">
← NEW REPORT
</button>

<button class="next-btn" onclick="goTo(5)">
VIEW INSIGHTS →
</button>

</div>

</div>

</section>


<!-- SCREEN 5 -->

<section class="screen" id="screen5">

<div class="page-title">

<small>STEP 05 / AI REVIEW LAYER</small>

<h2>Clinical Insights</h2>

<p>
A simplified view of information found in the source report.
</p>

</div>


<div class="dashboard">


<section class="card">

<div class="title">
<div class="icon">🧠</div>

<div>
<h3>Patient-Friendly Summary</h3>
<div class="sub">Factual source-based summary</div>
</div>

</div>

<div class="summary" id="summary"></div>

</section>


<section class="card">

<div class="title">
<div class="icon">⚠️</div>

<div>
<h3>Conflict Detection</h3>
<div class="sub">Items requiring human review</div>
</div>

</div>

<div id="conflicts"></div>

</section>

</div>


<section class="card" style="margin-top:18px">

<div class="title">

<div class="icon">🛡️</div>

<div>
<h3>Responsible AI</h3>
<div class="sub">Safety and transparency layer</div>
</div>

</div>


<div class="notice">

<strong>MedLens is a review-support tool.</strong>

<br><br>

It does not provide medical diagnosis, prescribe treatment,
recommend medication changes, or determine medication dosage.

<br><br>

LOW, NORMAL and HIGH are assigned only when a usable
reference range is available in the uploaded report.
Otherwise the result is UNKNOWN.

<br><br>

AI-extracted information should always be reviewed against
the original report by a qualified human before clinical use.

</div>


<div class="next-row">

<button class="back-btn" onclick="goTo(4)">
← RECORD
</button>

<button class="next-btn" onclick="newAnalysis()">
START NEW ANALYSIS ↻
</button>

</div>

</section>

</section>


<div class="footer">
<span>MedLens</span> · AI Clinical Information Intelligence · Human review required
</div>

</div>


<script>

let currentStep=0;
let analysisData=null;


function goTo(step){

 document.querySelectorAll(".screen").forEach(
  screen=>screen.classList.remove("active")
 );

 const target=document.getElementById("screen"+step);

 if(target){
  target.classList.add("active");
 }

 currentStep=step;

 updateProgress(step);

 window.scrollTo({
  top:0,
  behavior:"smooth"
 });

}


function updateProgress(step){

 const steps=document.querySelectorAll(".progress-step");
 const lines=document.querySelectorAll(".progress-line");

 steps.forEach((item,index)=>{

  item.classList.remove("active","done");

  if(index<step){
   item.classList.add("done");
  }

  if(index===step){
   item.classList.add("active");
  }

 });

 lines.forEach((line,index)=>{

  line.classList.toggle(
   "done",
   index<step
  );

 });

}


function escapeHTML(value){

 if(value===null||value===undefined){
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

 const value=String(
  status||"UNKNOWN"
 ).toUpperCase();

 let cls="unknown";

 if(value==="LOW")cls="low";
 if(value==="NORMAL")cls="normal";
 if(value==="HIGH")cls="high";

 return `
 <span
 class="badge ${cls}"
 aria-label="Status: ${escapeHTML(value)}">
 ${escapeHTML(value)}
 </span>
 `;

}


const reportInput=document.getElementById("report");
const uploadZone=document.getElementById("uploadZone");
const fileInfo=document.getElementById("fileInfo");


reportInput.addEventListener("change",function(){

 if(this.files.length){
  showFile(this.files[0]);
 }

});


function showFile(file){

 if(file.size>8*1024*1024){

  fileInfo.style.display="block";
  fileInfo.style.color="#ff416d";
  fileInfo.textContent=
   "✕ File exceeds the 8 MB limit.";

  return;
 }

 fileInfo.style.display="block";
 fileInfo.style.color="var(--lime)";

 fileInfo.textContent=
  "✓ "+file.name+
  " · "+formatBytes(file.size);

}


function formatBytes(bytes){

 if(bytes<1024){
  return bytes+" B";
 }

 if(bytes<1024*1024){
  return (bytes/1024).toFixed(1)+" KB";
 }

 return (bytes/(1024*1024)).toFixed(2)+" MB";

}


["dragenter","dragover"].forEach(eventName=>{

 uploadZone.addEventListener(
  eventName,
  event=>{
   event.preventDefault();
   uploadZone.classList.add("drag");
  }
 );

});


["dragleave","drop"].forEach(eventName=>{

 uploadZone.addEventListener(
  eventName,
  event=>{
   event.preventDefault();
   uploadZone.classList.remove("drag");
  }
 );

});


uploadZone.addEventListener("drop",event=>{

 const files=event.dataTransfer.files;

 if(files.length){

  reportInput.files=files;
  showFile(files[0]);

 }

});


function getPatient(){

 return {

  age:document.getElementById("age").value,

  sex:document.getElementById("sex").value,

  symptoms:document.getElementById("symptoms").value,

  conditions:document.getElementById("conditions").value,

  allergies:document.getElementById("allergies").value,

  medications:document.getElementById("medications").value

 };

}


async function startAnalysis(){

 const fileInput=document.getElementById("report");
 const button=document.getElementById("analyzeBtn");

 if(!fileInput.files.length){

  alert("Please choose a medical report first.");

  return;

 }


 const file=fileInput.files[0];


 if(file.size>8*1024*1024){

  alert("File is too large. Maximum allowed size is 8 MB.");

  return;

 }


 const formData=new FormData();

 formData.append(
  "file",
  file
 );

 formData.append(
  "patient",
  JSON.stringify(getPatient())
 );


 button.disabled=true;

 goTo(3);

 runProcessingAnimation();


 try{

  const response=await fetch(
   "/analyze",
   {
    method:"POST",
    body:formData
   }
  );


  let data;

  try{

   data=await response.json();

  }catch{

   throw new Error(
    "The server returned an unexpected response."
   );

  }


  if(data.error){

   throw new Error(data.error);

  }


  analysisData=data;

  renderRecord(data);
  renderInsights(data);


  setTimeout(()=>{
   goTo(4);
  },500);


 }catch(error){

  goTo(2);

  alert(
   error.message ||
   "Unable to process report."
  );


 }finally{

  button.disabled=false;

 }

}


function runProcessingAnimation(){

 const steps=[
  document.getElementById("p1"),
  document.getElementById("p2"),
  document.getElementById("p3"),
  document.getElementById("p4")
 ];

 const text=document.getElementById(
  "processingText"
 );

 steps.forEach(step=>{
  step.classList.remove("active","done");
  step.querySelector(".mark").textContent="○";
 });

 const messages=[
  "Reading the uploaded source document...",
  "Extracting tests, values and observations...",
  "Checking source-provided reference ranges...",
  "Building the structured medical record..."
 ];


 steps.forEach((step,index)=>{

  setTimeout(()=>{

   if(index>0){

    steps[index-1].classList.remove("active");
    steps[index-1].classList.add("done");
    steps[index-1].querySelector(".mark").textContent="✓";

   }

   step.classList.add("active");
   step.querySelector(".mark").textContent="◉";

   text.textContent=messages[index];

  },index*850);

 });

}


function renderRecord(data){

 const rows=document.getElementById("testRows");

 const tests=
  Array.isArray(data.tests)
  ?data.tests
  :[];


 document.getElementById(
  "testCount"
 ).textContent=
  tests.length+" TESTS";


 if(!tests.length){

  rows.innerHTML=`
   <tr>
   <td colspan="9" class="empty">
   No structured test results were extracted.
   </td>
   </tr>
  `;

  return;

 }


 rows.innerHTML=tests.map(
  (test,index)=>`

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

  </tr>

 `
 ).join("");

}


function renderInsights(data){

 document.getElementById(
  "summary"
 ).textContent=
  data.summary ||
  "No summary generated.";


 const container=
  document.getElementById("conflicts");


 const conflicts=
  Array.isArray(data.conflicts)
  ?data.conflicts
  :[];


 if(!conflicts.length){

  container.innerHTML=`
   <p class="empty">
   ✓ No conflicts were detected in the supplied information.
   </p>
  `;

  return;

 }


 container.innerHTML=
  conflicts.map(
   item=>`
   <div class="conflict" role="alert">
   ⚠️ ${escapeHTML(item)}
   </div>
   `
  ).join("");

}


function newAnalysis(){

 analysisData=null;

 document.getElementById("report").value="";

 document.getElementById("fileInfo").style.display="none";

 document.getElementById("summary").textContent="";

 document.getElementById("conflicts").innerHTML="";

 document.getElementById("testRows").innerHTML="";

 document.getElementById("age").value="";

 document.getElementById("sex").value="";

 document.getElementById("symptoms").value="";

 document.getElementById("conditions").value="";

 document.getElementById("allergies").value="";

 document.getElementById("medications").value="";

 goTo(0);

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

    encoded = base64.b64encode(
        file_bytes
    ).decode("utf-8")

    return f"data:{mime_type};base64,{encoded}"


def _numbers(value):

    if value is None:
        return []

    text = str(value).replace(",", "")

    found = re.findall(
        r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)",
        text
    )

    numbers=[]

    for item in found:

        try:
            numbers.append(float(item))

        except ValueError:
            pass

    return numbers


def _first_number(value):

    numbers=_numbers(value)

    return numbers[0] if numbers else None


def classify_from_reference(value, reference):

    value_text=str(value or "").strip()
    ref_text=str(reference or "").strip()

    if not value_text or not ref_text:
        return "UNKNOWN"

    value_clean=value_text.lower().replace("*","").strip()
    ref_clean=ref_text.lower().replace("*","").strip()


    # Qualitative references.
    if ref_clean in {
        "negative",
        "none",
        "absent",
        "not detected",
        "not seen",
        "nil",
        "normal",
        "clear",
        "occasional"
    }:

        if value_clean == ref_clean:
            return "NORMAL"

        return "HIGH"


    # <X and <=X
    upper=re.fullmatch(
        r"(?:less than|<|<=)\s*"
        r"([-+]?(?:\d+(?:\.\d*)?|\.\d+))",
        ref_clean
    )

    if upper:

        limit=float(
            upper.group(1)
        )

        actual=_first_number(
            value_clean
        )

        if actual is None:
            return "UNKNOWN"

        if "<=" in ref_clean:
            return "NORMAL" if actual<=limit else "HIGH"

        return "NORMAL" if actual<limit else "HIGH"


    # >X and >=X
    lower=re.fullmatch(
        r"(?:greater than|>|>=)\s*"
        r"([-+]?(?:\d+(?:\.\d*)?|\.\d+))",
        ref_clean
    )

    if lower:

        limit=float(
            lower.group(1)
        )

        actual=_first_number(
            value_clean
        )

        if actual is None:
            return "UNKNOWN"

        if ">=" in ref_clean:
            return "NORMAL" if actual>=limit else "LOW"

        return "NORMAL" if actual>limit else "LOW"


    # Numeric range.
    ref_numbers=_numbers(ref_clean)

    if len(ref_numbers)>=2:

        low=ref_numbers[0]
        high=ref_numbers[1]

        if low>high:
            low,high=high,low

        actual=_first_number(
            value_clean
        )

        if actual is None:
            return "UNKNOWN"

        if actual<low:
            return "LOW"

        if actual>high:
            return "HIGH"

        return "NORMAL"


    return "UNKNOWN"


def normalize_result(data):

    if not isinstance(data,dict):
        data={}

    tests=data.get("tests",[])

    if not isinstance(tests,list):
        tests=[]

    normalized_tests=[]


    for test in tests:

        if not isinstance(test,dict):
            continue


        test_name=str(
            test.get("test_name","")
        ).strip()

        value=str(
            test.get("value","")
        ).strip()

        unit=str(
            test.get("unit","")
        ).strip()

        reference_range=str(
            test.get("reference_range","")
        ).strip()

        date=str(
            test.get("date","")
        ).strip()

        observation=str(
            test.get("observation","")
        ).strip()

        source=str(
            test.get(
                "source",
                "uploaded report"
            )
        ).strip()


        ai_status=str(
            test.get(
                "status",
                "UNKNOWN"
            )
        ).upper().strip()


        if ai_status not in {
            "LOW",
            "NORMAL",
            "HIGH",
            "UNKNOWN"
        }:

            ai_status="UNKNOWN"


        calculated_status=classify_from_reference(
            value,
            reference_range
        )


        if calculated_status!="UNKNOWN":
            status=calculated_status
        else:
            status=ai_status


        if not reference_range:
            status="UNKNOWN"


        normalized_tests.append({

            "test_name":test_name,

            "value":value,

            "unit":unit,

            "reference_range":reference_range,

            "status":status,

            "date":date,

            "observation":observation,

            "source":
            source or "uploaded report"

        })


    conflicts=data.get(
        "conflicts",
        []
    )


    if not isinstance(
        conflicts,
        list
    ):

        conflicts=[
            str(conflicts)
        ]


    return {

        "tests":normalized_tests,

        "conflicts":[
            str(x)
            for x in conflicts
        ],

        "summary":str(
            data.get(
                "summary",
                ""
            )
        )

    }


@app.post("/analyze")
async def analyze(
    file:UploadFile=File(...),
    patient:str=Form("{}")
):

    api_key=os.getenv(
        "OPENROUTER_API_KEY"
    )


    if not api_key:

        return {
            "error":
            "OPENROUTER_API_KEY is not configured in Render."
        }


    allowed_types={
        "application/pdf",
        "image/jpeg",
        "image/png",
        "image/webp"
    }


    mime_type=(
        file.content_type
        or "application/octet-stream"
    )


    if mime_type not in allowed_types:

        return {
            "error":
            "Unsupported file type. Please upload PDF, JPG, PNG, or WEBP."
        }


    file_bytes=await file.read()


    if len(file_bytes)>8*1024*1024:

        return {
            "error":
            "File is too large. Maximum allowed size is 8 MB."
        }


    try:

        patient_data=json.loads(
            patient
        )

        if not isinstance(
            patient_data,
            dict
        ):
            patient_data={}

    except Exception:

        patient_data={}


    # Bound patient-provided text.
    for key in list(
        patient_data.keys()
    ):

        value=patient_data[key]

        if isinstance(
            value,
            str
        ):

            patient_data[key]=value[:1000]


    prompt=f"""
You are the extraction engine for MedLens,
a clinical information structuring application.

Read ONLY the uploaded medical report and convert
its contents into structured information.

PATIENT-PROVIDED INFORMATION:
{json.dumps(patient_data,ensure_ascii=False)}

STRICT RULES:

1. Extract medical test information ONLY from the uploaded report.
2. NEVER invent a laboratory value.
3. NEVER invent a unit.
4. NEVER invent a date.
5. NEVER invent a reference range.
6. Preserve source values and reference ranges as written.
7. LOW, NORMAL, or HIGH may ONLY be assigned when the
   uploaded report provides a reference range.
8. Numeric values below the source lower bound are LOW.
9. Numeric values inside the source range are NORMAL.
10. Numeric values above the source upper bound are HIGH.
11. For <X references, values outside the upper limit are HIGH.
12. For >X references, values outside the lower limit are LOW.
13. For qualitative references such as Negative, None or Absent,
    compare only according to the wording shown in the report.
14. If comparison is not unambiguous, use UNKNOWN.
15. NEVER use general medical knowledge to create a range.
16. Do not diagnose or speculate about disease.
17. If the report itself mentions a diagnosis or interpretation,
    reproduce it only as "The report states..." or
    "The report mentions...".
18. Do not recommend treatment.
19. Do not recommend medication changes.
20. Do not recommend dosage changes.
21. Detect obvious contradictions between patient information
    and information explicitly present in the report.
22. Missing optional patient information is NOT a conflict.
23. Keep the summary concise, factual and patient-friendly.
24. Do not add information not present in the source.

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

Do not use markdown.
"""


    data_url=make_data_url(
        file_bytes,
        mime_type
    )


    headers={
        "Authorization":
        f"Bearer {api_key}",

        "Content-Type":
        "application/json"
    }


    if mime_type=="application/pdf":

        content=[

            {
                "type":"text",
                "text":prompt
            },

            {
                "type":"file",
                "file":{

                    "filename":
                    file.filename or
                    "medical_report.pdf",

                    "file_data":
                    data_url

                }
            }

        ]

    else:

        content=[

            {
                "type":"text",
                "text":prompt
            },

            {
                "type":"image_url",
                "image_url":{
                    "url":data_url
                }
            }

        ]


    payload={

        "model":
        "minimax/minimax-m3:free",

        "messages":[

            {
                "role":"user",
                "content":content
            }

        ],

        "temperature":0.1,

        "max_tokens":2500

    }


    try:

        response=requests.post(

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


        result=response.json()

        choices=result.get(
            "choices",
            []
        )


        if not choices:

            return {
                "error":
                "OpenRouter returned no model response."
            }


        message=choices[0].get(
            "message",
            {}
        )


        content=message.get(
            "content",
            ""
        )


        if isinstance(
            content,
            list
        ):

            parts=[]

            for item in content:

                if (
                    isinstance(item,dict)
                    and "text" in item
                ):

                    parts.append(
                        str(item["text"])
                    )

                else:

                    parts.append(
                        str(item)
                    )

            content="".join(parts)


        content=str(content)

        cleaned=clean_json_text(
            content
        )


        try:

            parsed=json.loads(
                cleaned
            )

        except Exception:

            return {

                "error":
                (
                    "The AI returned an unexpected format. "
                    f"Raw response: {content[:1000]}"
                )

            }


        return normalize_result(
            parsed
        )


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
