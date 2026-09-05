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
 --bg:#050505;
 --panel:#0d0d11;
 --panel2:#121218;
 --text:#f4f4f5;
 --muted:#92929d;
 --lime:#c8ff00;
 --pink:#ff2bd6;
 --violet:#9b5cff;
 --yellow:#ffb800;
 --red:#ff416d;
 --line:rgba(200,255,0,.16);
}

html{scroll-behavior:smooth}

body{
 margin:0;
 color:var(--text);
 font-family:Inter,"Segoe UI",Arial,sans-serif;
 background:
 radial-gradient(circle at 8% 4%,rgba(200,255,0,.09),transparent 23%),
 radial-gradient(circle at 92% 8%,rgba(255,43,214,.11),transparent 25%),
 radial-gradient(circle at 50% 100%,rgba(155,92,255,.09),transparent 35%),
 var(--bg);
 min-height:100vh;
 overflow-x:hidden;
}

body:before{
 content:"";
 position:fixed;
 inset:0;
 pointer-events:none;
 background-image:
 linear-gradient(rgba(200,255,0,.022) 1px,transparent 1px),
 linear-gradient(90deg,rgba(255,43,214,.018) 1px,transparent 1px);
 background-size:42px 42px;
 mask-image:linear-gradient(to bottom,black,transparent 90%);
}

.header{
 position:relative;
 z-index:2;
 border-bottom:1px solid rgba(200,255,0,.13);
 background:rgba(5,5,5,.9);
 backdrop-filter:blur(20px);
 padding:22px 20px;
}

.header-inner,.container,.hero{
 max-width:1160px;
 margin:auto;
}

.header-inner{
 display:flex;
 align-items:center;
 justify-content:space-between;
 gap:20px;
}

.brand{display:flex;align-items:center;gap:14px}

.logo{
 width:56px;height:56px;
 display:grid;place-items:center;
 border-radius:17px;
 font-size:27px;
 background:linear-gradient(135deg,rgba(200,255,0,.12),rgba(255,43,214,.15));
 border:1px solid rgba(200,255,0,.4);
 box-shadow:0 0 35px rgba(200,255,0,.1);
}

h1{
 margin:0;
 font-size:34px;
 letter-spacing:-1.5px;
}

h1 .lime{color:var(--lime)}
h1 .pink{color:var(--pink)}

.header p{
 margin:6px 0 0;
 color:var(--muted);
 font-size:11px;
 letter-spacing:.7px;
}

.system{
 display:flex;
 align-items:center;
 gap:8px;
 padding:8px 13px;
 border:1px solid rgba(200,255,0,.25);
 border-radius:30px;
 color:var(--lime);
 background:rgba(200,255,0,.04);
 font-size:9px;
 font-weight:900;
 letter-spacing:.8px;
}

.system-dot{
 width:7px;height:7px;border-radius:50%;
 background:var(--lime);
 box-shadow:0 0 14px var(--lime);
}

.hero{
 padding:50px 20px 27px;
}

.kicker{
 display:inline-block;
 padding:7px 12px;
 border:1px solid rgba(255,43,214,.35);
 border-radius:30px;
 background:rgba(255,43,214,.05);
 color:#ff65e2;
 font-size:9px;
 font-weight:900;
 letter-spacing:1px;
}

.hero h2{
 margin:16px 0 10px;
 max-width:850px;
 font-size:clamp(38px,6vw,62px);
 line-height:1;
 letter-spacing:-3px;
}

.hero h2 span{
 background:linear-gradient(90deg,var(--lime),var(--pink),var(--violet));
 -webkit-background-clip:text;
 background-clip:text;
 color:transparent;
}

.hero p{
 max-width:760px;
 margin:0;
 color:var(--muted);
 line-height:1.7;
 font-size:14px;
}

.pipeline{
 display:flex;
 align-items:center;
 gap:10px;
 margin-top:22px;
 overflow-x:auto;
 padding-bottom:5px;
}

.step{
 display:flex;
 align-items:center;
 gap:7px;
 white-space:nowrap;
 color:#73737d;
 font-size:9px;
 font-weight:900;
}

.step b{
 width:26px;height:26px;
 display:grid;place-items:center;
 border-radius:50%;
 border:1px solid rgba(200,255,0,.3);
 color:var(--lime);
 background:rgba(200,255,0,.04);
}

.step-line{
 width:45px;
 height:1px;
 background:linear-gradient(90deg,var(--lime),var(--pink));
 opacity:.5;
}

.container{padding:0 20px}

.card{
 position:relative;
 overflow:hidden;
 margin-bottom:20px;
 padding:25px;
 border-radius:21px;
 border:1px solid var(--line);
 background:linear-gradient(145deg,rgba(16,16,20,.96),rgba(7,7,9,.95));
 box-shadow:0 25px 75px rgba(0,0,0,.58);
 backdrop-filter:blur(18px);
}

.card:before{
 content:"";
 position:absolute;
 top:0;left:28px;right:28px;
 height:1px;
 background:linear-gradient(90deg,transparent,var(--lime),var(--pink),transparent);
 opacity:.7;
}

.card:hover{
 border-color:rgba(200,255,0,.25);
}

.title{
 display:flex;
 align-items:center;
 gap:12px;
 margin-bottom:20px;
}

.icon{
 width:42px;height:42px;
 display:grid;place-items:center;
 border-radius:13px;
 background:linear-gradient(135deg,rgba(200,255,0,.08),rgba(255,43,214,.1));
 border:1px solid rgba(200,255,0,.18);
 font-size:18px;
}

h3{margin:0;font-size:18px}
.sub{margin-top:4px;color:var(--muted);font-size:11px}

.grid{
 display:grid;
 grid-template-columns:repeat(2,1fr);
 gap:15px;
}

.full{grid-column:1/-1}

label{
 display:block;
 margin-bottom:7px;
 color:#b7b7c0;
 font-size:9px;
 font-weight:900;
 letter-spacing:.8px;
}

input,textarea,select{
 width:100%;
 padding:13px;
 border-radius:11px;
 border:1px solid rgba(255,255,255,.1);
 outline:none;
 background:#08080a;
 color:var(--text);
 font-size:13px;
}

input::placeholder,textarea::placeholder{color:#50505a}

input:focus,textarea:focus,select:focus{
 border-color:rgba(200,255,0,.7);
 box-shadow:0 0 0 3px rgba(200,255,0,.05),0 0 25px rgba(200,255,0,.06);
}

input:focus-visible,textarea:focus-visible,select:focus-visible,
button:focus-visible,.file-label:focus-visible{
 outline:2px solid var(--lime);
 outline-offset:3px;
}

textarea{min-height:78px;resize:vertical}
select option{background:#111}

.upload{
 padding:35px 20px;
 text-align:center;
 border:1px dashed rgba(200,255,0,.4);
 border-radius:17px;
 background:
 radial-gradient(circle at 50% 20%,rgba(200,255,0,.07),transparent 45%),
 rgba(5,5,7,.7);
 transition:.2s;
}

.upload:hover{
 border-color:var(--pink);
 box-shadow:inset 0 0 40px rgba(255,43,214,.035);
}

.upload-icon{
 width:62px;height:62px;
 margin:auto auto 12px;
 display:grid;place-items:center;
 border-radius:19px;
 background:linear-gradient(135deg,rgba(200,255,0,.1),rgba(255,43,214,.12));
 border:1px solid rgba(200,255,0,.2);
 font-size:26px;
}

.upload strong{display:block;font-size:15px}
.upload p{margin:6px 0;color:var(--muted);font-size:12px}
.upload small{color:#62626c}

#report{
 display:block;
 width:100%;
 margin-top:12px;
 padding:7px;
}

.file-label{
 display:inline-block;
 margin-top:10px;
 padding:10px 17px;
 border-radius:10px;
 border:1px solid rgba(255,43,214,.4);
 color:#ff65e2;
 background:rgba(255,43,214,.045);
 cursor:pointer;
 font-size:11px;
 font-weight:900;
}

.file-label:hover{
 border-color:var(--pink);
 box-shadow:0 0 25px rgba(255,43,214,.1);
}

.primary{
 width:100%;
 margin-top:18px;
 padding:16px;
 border:1px solid rgba(200,255,0,.5);
 border-radius:12px;
 color:#050505;
 background:linear-gradient(100deg,#b7ee00,#c8ff00,#ff2bd6,#9b5cff);
 background-size:220% 100%;
 font-size:13px;
 font-weight:900;
 cursor:pointer;
 transition:.25s;
 box-shadow:0 10px 35px rgba(200,255,0,.1);
}

.primary:hover{
 background-position:100% 0;
 transform:translateY(-2px);
 box-shadow:0 15px 45px rgba(255,43,214,.14);
}

.primary:disabled{opacity:.55;cursor:wait;transform:none}

.status{
 min-height:20px;
 margin-top:12px;
 text-align:center;
 color:var(--lime);
 font-size:11px;
}

.status.error{color:var(--red)}

.results-head{
 display:flex;
 justify-content:space-between;
 margin:30px 0 13px;
 color:#71717b;
 font-size:9px;
 font-weight:900;
 letter-spacing:1px;
}

.results-head span{color:var(--lime)}

.table-wrap{
 overflow-x:auto;
 border:1px solid rgba(200,255,0,.12);
 border-radius:13px;
}

table{
 width:100%;
 min-width:960px;
 border-collapse:collapse;
}

caption{
 padding:10px;
 text-align:left;
 color:var(--muted);
 font-size:10px;
}

th,td{
 padding:12px;
 text-align:left;
 vertical-align:top;
 border-bottom:1px solid rgba(255,255,255,.06);
 font-size:11px;
}

th{
 background:rgba(200,255,0,.035);
 color:#b7d878;
 font-size:9px;
 text-transform:uppercase;
 letter-spacing:.6px;
}

td{color:#d7d7df}

tr:hover td{background:rgba(200,255,0,.018)}

.badge{
 display:inline-block;
 min-width:62px;
 padding:5px 8px;
 text-align:center;
 border-radius:20px;
 font-size:8px;
 font-weight:900;
 letter-spacing:.5px;
}

.normal{
 color:var(--lime);
 background:rgba(200,255,0,.07);
 border:1px solid rgba(200,255,0,.22);
}

.low{
 color:var(--yellow);
 background:rgba(255,184,0,.08);
 border:1px solid rgba(255,184,0,.2);
}

.high{
 color:#ff5278;
 background:rgba(255,65,109,.08);
 border:1px solid rgba(255,65,109,.22);
}

.unknown{
 color:#aaaab2;
 background:rgba(150,150,160,.06);
 border:1px solid rgba(150,150,160,.14);
}

.dashboard{
 display:grid;
 grid-template-columns:1.5fr .8fr;
 gap:20px;
}

.summary{
 padding:18px;
 border-radius:13px;
 line-height:1.7;
 color:#d8d8df;
 font-size:12px;
 background:linear-gradient(135deg,rgba(200,255,0,.035),rgba(255,43,214,.045));
 border:1px solid rgba(200,255,0,.12);
}

.conflict{
 padding:13px;
 margin:8px 0;
 border-radius:10px;
 border:1px solid rgba(255,184,0,.18);
 border-left:3px solid var(--yellow);
 background:rgba(255,184,0,.045);
 color:#dfd0a7;
 font-size:11px;
 line-height:1.55;
}

.notice{
 padding:17px;
 border-radius:12px;
 border:1px solid rgba(200,255,0,.13);
 border-left:3px solid var(--lime);
 background:linear-gradient(135deg,rgba(200,255,0,.035),rgba(155,92,255,.035));
 color:#c9c9d1;
 line-height:1.65;
 font-size:11px;
}

.notice strong{color:var(--lime)}

.empty{color:#686873;padding:10px 0;font-size:11px}

.footer{
 padding:18px 0 38px;
 text-align:center;
 color:#4d4d56;
 font-size:9px;
}

.footer span{color:var(--pink)}

@media(max-width:850px){
 .dashboard{grid-template-columns:1fr}
}

@media(max-width:700px){
 .grid{grid-template-columns:1fr}
 .full{grid-column:auto}
 .system{display:none}
 .hero{padding-top:35px}
 .hero h2{font-size:40px}
 .card{padding:20px}
}
</style>
</head>

<body>

<header class="header">
<div class="header-inner">

<div class="brand">
<div class="logo" aria-hidden="true">🧬</div>
<div>
<h1><span class="lime">Med</span><span class="pink">Lens</span></h1>
<p>AI CLINICAL INFORMATION INTELLIGENCE</p>
</div>
</div>

<div class="system">
<span class="system-dot"></span>
AI SYSTEM ONLINE
</div>

</div>
</header>


<section class="hero">

<div class="kicker">◈ MULTIMODAL AI · STRUCTURED CLINICAL DATA</div>

<h2>
Your reports.<br>
<span>Structured intelligence.</span>
</h2>

<p>
Transform medical reports into structured, reviewable information
with reference-aware extraction, conflict detection and
patient-friendly summaries — while keeping human verification
at the center.
</p>

<div class="pipeline" aria-label="Processing workflow">

<div class="step"><b>01</b>PATIENT</div>
<div class="step-line"></div>

<div class="step"><b>02</b>REPORT</div>
<div class="step-line"></div>

<div class="step"><b>03</b>AI EXTRACT</div>
<div class="step-line"></div>

<div class="step"><b>04</b>REVIEW</div>

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
<textarea id="symptoms"
placeholder="Enter patient-reported symptoms"></textarea>
</div>

<div>
<label for="conditions">KNOWN CONDITIONS</label>
<textarea id="conditions"
placeholder="Existing conditions"></textarea>
</div>

<div>
<label for="allergies">ALLERGIES</label>
<textarea id="allergies"
placeholder="Known allergies"></textarea>
</div>

<div class="full">
<label for="medications">CURRENT MEDICATIONS</label>
<textarea id="medications"
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

<small id="report-help">Maximum file size: 8 MB</small>

<label for="report" class="file-label">
Choose medical report
</label>

<input id="report"
type="file"
accept=".pdf,.jpg,.jpeg,.png,.webp"
aria-describedby="report-help">

</div>

<button
id="processBtn"
class="primary"
type="button"
onclick="processReport()"
aria-describedby="status">

⚡ PROCESS MEDICAL REPORT

</button>

<div id="status"
class="status"
role="status"
aria-live="polite"
aria-atomic="true"></div>

</section>


<div id="results" aria-live="polite"></div>


<div class="footer">
<span>MedLens</span> · Clinical information structuring · Human review required
</div>

</main>


<script>

function escapeHTML(value){
 if(value===null||value===undefined)return "";
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

 if(value==="LOW")cls="low";
 if(value==="NORMAL")cls="normal";
 if(value==="HIGH")cls="high";

 return `
 <span class="badge ${cls}" aria-label="Status: ${escapeHTML(value)}">
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
  button.textContent="⚡ PROCESS MEDICAL REPORT";

 }
}


function renderResults(data){

 const results=document.getElementById("results");
 const tests=Array.isArray(data.tests)?data.tests:[];

 let rows="";

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
 Array.isArray(data.conflicts)?data.conflicts:[];

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
 <div>ANALYSIS <span>COMPLETE</span></div>
 <div>${tests.length} TESTS EXTRACTED</div>
 </div>

 <section class="card" aria-labelledby="record-heading">

 <div class="title">
 <div class="icon" aria-hidden="true">📊</div>
 <div>
 <h3 id="record-heading">Structured Medical Record</h3>
 <div class="sub">AI-extracted information from the uploaded source</div>
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

 <tbody>${rows}</tbody>

 </table>
 </div>

 </section>


 <div class="dashboard">

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


def _first_number(value):

    numbers = _numbers(value)

    return numbers[0] if numbers else None


def classify_from_reference(value, reference):

    value_text = str(value or "").strip()
    ref_text = str(reference or "").strip()

    if not value_text or not ref_text:
        return "UNKNOWN"

    value_clean = value_text.lower().replace("*","").strip()
    ref_clean = ref_text.lower().replace("*","").strip()

    # Direct qualitative reference comparisons.
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


    # <140 / <=140
    upper = re.fullmatch(
        r"(?:less than|<|<=)\s*([-+]?(?:\d+(?:\.\d*)?|\.\d+))",
        ref_clean
    )

    if upper:

        limit = float(upper.group(1))
        actual = _first_number(value_clean)

        if actual is None:
            return "UNKNOWN"

        if "<=" in ref_clean:
            return "NORMAL" if actual <= limit else "HIGH"

        return "NORMAL" if actual < limit else "HIGH"


    # >5 / >=5
    lower = re.fullmatch(
        r"(?:greater than|>|>=)\s*([-+]?(?:\d+(?:\.\d*)?|\.\d+))",
        ref_clean
    )

    if lower:

        limit = float(lower.group(1))
        actual = _first_number(value_clean)

        if actual is None:
            return "UNKNOWN"

        if ">=" in ref_clean:
            return "NORMAL" if actual >= limit else "LOW"

        return "NORMAL" if actual > limit else "LOW"


    # Numeric ranges such as 5.0-8.0 or 5.0–8.0.
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

        if ai_status not in {
            "LOW",
            "NORMAL",
            "HIGH",
            "UNKNOWN"
        }:
            ai_status = "UNKNOWN"


        # Deterministic reference-range validation.
        calculated_status = classify_from_reference(
            value,
            reference_range
        )

        if calculated_status != "UNKNOWN":
            status = calculated_status
        else:
            status = ai_status


        # Never allow a status without a source reference.
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


    # Bound user-provided text for efficiency.
    for key in list(patient_data.keys()):

        value = patient_data[key]

        if isinstance(value, str):
            patient_data[key] = value[:1000]


    prompt = f"""
You are the extraction engine for MedLens,
a clinical information structuring application.

Read ONLY the uploaded medical report and convert
its contents into structured information.

PATIENT-PROVIDED INFORMATION:
{json.dumps(patient_data, ensure_ascii=False)}

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
11. For <X references, values outside the stated upper limit are HIGH.
12. For >X references, values outside the stated lower limit are LOW.
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
