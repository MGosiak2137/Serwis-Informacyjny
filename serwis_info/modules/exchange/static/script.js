(function(){
  function showTab(name){
    document.querySelectorAll('.tab-btn').forEach(b=>b.classList.remove('active'));
    document.querySelectorAll('.tab-panel').forEach(p=>p.style.display='none');
    var btn=document.getElementById('tab-'+name);
    var panel=document.getElementById('tab-content-'+name);
    if(btn)btn.classList.add('active');
    if(panel)panel.style.display='block';
    var leftOptions=document.getElementById('left-options');
    var leftCards=document.getElementById('left-cards');
    function hideAll(){ document.querySelectorAll('.chart-container').forEach(el=>el.style.display='none'); document.querySelectorAll('[id^="intraday-"]').forEach(el=>el.style.display='none'); var rb=document.querySelector('.range-buttons'); if(rb)rb.style.display='none'; }
    function showRange(){ var rb=document.querySelector('.range-buttons'); if(rb)rb.style.display=''; }
    if(name==='category'){ hideAll(); if(leftOptions)leftOptions.style.display='none'; if(leftCards)leftCards.style.display='none'; var sel=document.getElementById('select-symbols'); if(sel)Array.from(sel.options).forEach(o=>o.selected=false); return; }
    if(name==='options'){ hideAll(); if(leftOptions)leftOptions.style.display='block'; if(leftCards)leftCards.style.display='none'; return; }
    if(name==='results'){ if(leftOptions)leftOptions.style.display='none'; if(leftCards)leftCards.style.display='block'; showRange(); var init=document.getElementById('stockmarket-init'); var selSyms=(init&&init.dataset.selectedSymbols)?init.dataset.selectedSymbols.split(',').filter(Boolean):[]; showOnlySelectedCards(selSyms); displayFirstAvailableChart(selSyms); return; }
  }

  function loadSelected(){
    var select=document.getElementById('select-symbols');
    var symbols=[];
    if(select)Array.from(select.options).forEach(opt=>{ if(opt.selected) symbols.push(opt.value); });
    if(symbols.length===0){ alert('Wybierz przynajmniej jeden symbol z listy.'); return; }
    var q=new URLSearchParams();
    q.set('symbols', symbols.join(','));
    var init=document.getElementById('stockmarket-init');
    if(init){ var range=init.dataset.currentRange||''; var cat=init.dataset.selectedCategory||''; if(range) q.set('range', range); if(cat) q.set('category', cat); }
    window.location='/stockmarket?'+q.toString();
  }

  function toggleChart(symbol){
    if(!symbol) return;
    document.querySelectorAll('.chart-container').forEach(el=>el.style.display='none');
    document.querySelectorAll('[id^="intraday-"]').forEach(el=>el.style.display='none');
    var chart=document.getElementById('chart-'+symbol);
    var intr=document.getElementById('intraday-'+symbol);
    if(chart) chart.style.display='block';
    if(intr) intr.style.display='block';
    if(chart) chart.scrollIntoView({behavior:'smooth', block:'center'});
  }

  function showOnlySelectedCards(selectedArray){
    var cards=document.querySelectorAll('#left-cards .index-card');
    if(!selectedArray||selectedArray.length===0){ cards.forEach(c=>{ c.style.display=''; c.classList.remove('disabled-card'); }); return; }
    var set=new Set(selectedArray);
    cards.forEach(c=>{ var sym=c.dataset.symbol; if(set.has(sym)){ c.style.display=''; if(!c.classList.contains('disabled-card')) c.classList.add('disabled-card'); } else c.style.display='none'; });
  }

  function displayFirstAvailableChart(selectedArray){
    document.querySelectorAll('.chart-container').forEach(el=>el.style.display='none');
    document.querySelectorAll('[id^="intraday-"]').forEach(el=>el.style.display='none');
    if(selectedArray&&selectedArray.length){
      for(var i=0;i<selectedArray.length;i++){
        var sym=selectedArray[i];
        try{ var c=document.getElementById('chart-'+sym); if(c){ var intr=document.getElementById('intraday-'+sym); c.style.display='block'; if(intr) intr.style.display='block'; c.scrollIntoView({behavior:'smooth', block:'center'}); return true; } }catch(e){}
      }
    }
    var first=document.querySelector('.chart-container');
    if(first){ first.style.display='block'; var id=first.id||''; if(id.startsWith('chart-')){ var s=id.slice(6); var intr=document.getElementById('intraday-'+s); if(intr) intr.style.display='block'; } first.scrollIntoView({behavior:'smooth', block:'center'}); return true; }
    return false;
  }

  function renderTicker(items){
    var track=document.getElementById('live-ticker');
    if(!track) return;
    track.innerHTML='';
    items.forEach(function(it){
      var div=document.createElement('div');
      div.className='ticker-item';
      if(it.rate&&it.rate.startsWith('+')) div.classList.add('positive');
      if(it.rate&&it.rate.startsWith('-')) div.classList.add('negative');
      var price=(it.price===null||it.price===undefined)?'n/d':Number(it.price).toFixed(2);
      div.textContent=it.name+' '+price+' '+(it.rate||'');
      track.appendChild(div);
    });
  }

  function refreshTicker(){
    fetch('/stockmarket/ticker').then(r=>r.json()).then(data=>{ renderTicker(data||[]); }).catch(()=>{}).finally(()=>{ setTimeout(refreshTicker,30000); });
  }

  document.addEventListener('DOMContentLoaded',function(){
    var init=document.getElementById('stockmarket-init');
    var initSyms=(init&&init.dataset.selectedSymbols)?init.dataset.selectedSymbols.split(',').filter(Boolean):[];
    if(initSyms&&initSyms.length){ showTab('results'); displayFirstAvailableChart(initSyms); }
    else if(init&&init.dataset.selectedCategory){ showTab('options'); }
    else showTab('category');
    window.showTab=showTab; window.loadSelected=loadSelected; window.toggleChart=toggleChart;
    var loadBtn=document.getElementById('load-selected-btn'); if(loadBtn) loadBtn.addEventListener('click', loadSelected);
    refreshTicker();
  });
})();
