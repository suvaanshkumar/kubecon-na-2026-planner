
const fs=require("fs");
const DATE={sun:"20261108",mon:"20261109",tue:"20261110",wed:"20261111",thu:"20261112",fri:"20261113"};
const esc=t=>String(t||"").replace(/\\/g,"\\\\").replace(/;/g,"\\;").replace(/,/g,"\\,").replace(/\r?\n/g,"\\n");
const fold=line=>{
  const b=Buffer.from(line,"utf8");
  if(b.length<=75)return line;
  const out=[];let i=0,first=true;
  while(i<b.length){
    const n=first?75:74;let end=Math.min(i+n,b.length);
    while(end<b.length&&(b[end]&0xC0)===0x80)end--;
    out.push((first?"":" ")+b.slice(i,end).toString("utf8"));i=end;first=false;
  }
  return out.join("\r\n");
};
const dt=(day,t)=>DATE[day]+"T"+t.replace(":","")+"00";
const L=["BEGIN:VCALENDAR","VERSION:2.0","PRODID:-//KubeCon NA 2026 plan//EN","CALSCALE:GREGORIAN","METHOD:PUBLISH","X-WR-CALNAME:KubeCon NA 2026 (MST)","X-WR-TIMEZONE:America/Denver",
"BEGIN:VTIMEZONE","TZID:America/Denver","BEGIN:STANDARD","DTSTART:19701101T020000","RRULE:FREQ=YEARLY;BYMONTH=11;BYDAY=1SU","TZOFFSETFROM:-0600","TZOFFSETTO:-0700","TZNAME:MST","END:STANDARD",
"BEGIN:DAYLIGHT","DTSTART:19700308T020000","RRULE:FREQ=YEARLY;BYMONTH=3;BYDAY=2SU","TZOFFSETFROM:-0700","TZOFFSETTO:-0600","TZNAME:MDT","END:DAYLIGHT","END:VTIMEZONE"];
let n=0;
for(const d of DAYS)for(const e of entries(d.k)){
  const desc=[e.note,e.url?("Details: "+e.url):"",e.confirm?"CONFIRM this one before relying on it.":""].filter(Boolean).join("\n");
  const alarm=e.kind==="talk"?30:e.kind==="booth"?20:10;
  L.push("BEGIN:VEVENT","UID:kubecon26-"+e.id+"@plan.local","DTSTAMP:20261107T000000Z",
   "DTSTART;TZID=America/Denver:"+dt(d.k,e.start),"DTEND;TZID=America/Denver:"+dt(d.k,e.end),
   "SUMMARY:"+esc((e.kind==="booth"?"[Booth] ":e.kind==="talk"?"[My talk] ":"")+e.title),
   "LOCATION:"+esc(e.loc),"DESCRIPTION:"+esc(desc),"CATEGORIES:"+esc(KINDS[e.kind]||"Other"),
   "BEGIN:VALARM","ACTION:DISPLAY","DESCRIPTION:"+esc(e.title),"TRIGGER:-PT"+alarm+"M","END:VALARM","END:VEVENT");
  n++;
}
for(const d of DAYS){
  const lb=leaveBy(d.k);if(!lb)continue;
  const m=mins(lb.time);
  L.push("BEGIN:VEVENT","UID:kubecon26-leave-"+d.k+"@plan.local","DTSTAMP:20261107T000000Z",
   "DTSTART;TZID=America/Denver:"+dt(d.k,lb.time),"DTEND;TZID=America/Denver:"+dt(d.k,toHHMM(m+15)),
   "SUMMARY:"+esc("Leave the hotel"),"LOCATION:"+esc(HOTEL),"DESCRIPTION:"+esc("Leave "+lb.why+". Travel times are estimates."),
   "BEGIN:VALARM","ACTION:DISPLAY","DESCRIPTION:Leave the hotel","TRIGGER:-PT10M","END:VALARM","END:VEVENT");
  n++;
}
L.push("END:VCALENDAR");
fs.writeFileSync(process.env.ICS_OUT,L.map(fold).join("\r\n")+"\r\n");
console.log(n+" events written");
