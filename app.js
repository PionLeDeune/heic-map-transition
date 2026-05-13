let map = L.map('map').setView([0, 0], 2);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
}).addTo(map);

const thumbs = document.getElementById('thumbs');

function loadData(){
    fetch('/data').then(r=>r.json()).then(data=>{
        if(!data || data.length===0) return;
        const group = L.featureGroup();
        data.forEach((p, idx)=>{
            const marker = L.marker([p.lat, p.lon]).addTo(map);
            marker.bindPopup(`<b>${p.name}</b><br>${p.lat.toFixed(6)}, ${p.lon.toFixed(6)}`);
            marker._photoIndex = idx;
            marker.on('click', ()=>{
                highlightThumb(idx);
            });

            const div = document.createElement('div');
            div.className = 'thumb';
            div.dataset.idx = idx;
            if(p.thumb){
                const img = document.createElement('img');
                img.src = p.thumb;
                div.appendChild(img);
            } else {
                div.textContent = p.name;
            }
            div.addEventListener('click', ()=>{
                map.setView([p.lat, p.lon], 18);
                marker.openPopup();
                highlightThumb(idx);
            });
            thumbs.appendChild(div);

            group.addLayer(marker);
        });
        map.fitBounds(group.getBounds(), {padding:[50,50]});
    });
}

function highlightThumb(idx){
    document.querySelectorAll('.thumb').forEach(t=>t.classList.remove('active'));
    const el = document.querySelector(`.thumb[data-idx='${idx}']`);
    if(el){ el.classList.add('active'); el.scrollIntoView({behavior:'smooth', block:'center'}); }
}

document.getElementById('scanForm').addEventListener('submit', (e)=>{
    e.preventDefault();
    const folder = document.getElementById('folderInput').value.trim();
    if(!folder) return alert('请输入文件夹路径');
    fetch('/scan', {method:'POST', headers:{'Content-Type':'application/x-www-form-urlencoded'}, body:`folder=${encodeURIComponent(folder)}`})
        .then(r=>r.json()).then(res=>{
            if(res.error) return alert('扫描失败: '+res.error);
            thumbs.innerHTML='';
            loadData();
            alert('扫描完成，找到 '+res.count+' 张带 GPS 的图片');
        }).catch(err=>alert('请求失败:'+err));
});

loadData();
