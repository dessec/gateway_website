// map.js
// Ensure mapboxgl and THREE are available from CDN scripts

mapboxgl.accessToken = 'pk.eyJ1IjoiYnJhZGw3IiwiYSI6ImNtbTgweHlwcDBkZGMycXE5eG9mc2pmeTcifQ.XuZc8Go52VITh6mhvx51yQ';

const map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/standard',
    center: [-79.8711, 43.2557], // Southern Ontario (Hamilton area)
    zoom: 9,
    pitch: 45,
    bearing: -17,
    antialias: true
});

let pinsData = [];

map.on('style.load', () => {
    // Add 3D Terrain
    map.addSource('mapbox-dem', {
        'type': 'raster-dem',
        'url': 'mapbox://mapbox.mapbox-terrain-dem-v1',
        'tileSize': 512,
        'maxzoom': 14
    });
    map.setTerrain({ 'source': 'mapbox-dem', 'exaggeration': 1.5 });

    // Fetch Pins and initialize Custom 3D Layer
    fetch('pins.json')
        .then(res => res.json())
        .then(data => {
            pinsData = data;
            initCustomLayer();
        })
        .catch(err => {
            console.error('Error loading pins:', err);
            initCustomLayer();
        });
});

// Custom 3D Layer implementation using Three.js as requested
let renderers = [];
const customLayerId = '3d-markers';

function initCustomLayer() {
    const customLayer = {
        id: customLayerId,
        type: 'custom',
        renderingMode: '3d',
        onAdd: function (map, gl) {
            this.camera = new THREE.Camera();
            this.scene = new THREE.Scene();

            // Lighting
            const dirLight = new THREE.DirectionalLight(0xffffff, 2);
            dirLight.position.set(0, -70, 100).normalize();
            this.scene.add(dirLight);

            const dirLight2 = new THREE.DirectionalLight(0xffffff, 2);
            dirLight2.position.set(0, 70, 100).normalize();
            this.scene.add(dirLight2);

            this.scene.add(new THREE.AmbientLight(0x404040, 2));

            this.map = map;

            // Use the Mapbox GL Context to setup WebGLRenderer
            this.renderer = new THREE.WebGLRenderer({
                canvas: map.getCanvas(),
                context: gl,
                antialias: true
            });

            this.renderer.autoClear = false;

            // Store meshes for raycasting
            this.meshes = [];

            // Load model and place at each pin
            const loader = new THREE.GLTFLoader();

            pinsData.forEach((pin, index) => {
                const modelOrigin = [pin.lng, pin.lat];
                const modelAltitude = 0;
                const modelRotate = [Math.PI / 2, 0, 0];

                const modelAsMercatorCoordinate = mapboxgl.MercatorCoordinate.fromLngLat(
                    modelOrigin,
                    modelAltitude
                );

                const modelTransform = {
                    translateX: modelAsMercatorCoordinate.x,
                    translateY: modelAsMercatorCoordinate.y,
                    translateZ: modelAsMercatorCoordinate.z,
                    rotateX: modelRotate[0],
                    rotateY: modelRotate[1],
                    rotateZ: modelRotate[2],
                    scale: modelAsMercatorCoordinate.meterInMercatorCoordinateUnits() * 10 // scale up so it's visible
                };

                // Fallback geometry if GLB fails
                const material = new THREE.MeshPhongMaterial({ color: 0xc8972a });
                const geometry = new THREE.ConeGeometry(0.5, 2, 8);
                geometry.translate(0, 1, 0); // anchor at bottom
                // Rotate to stand upright in mapbox coords
                geometry.rotateX(Math.PI / 2);

                loader.load(
                    'assets/flag-marker.glb',
                    (gltf) => {
                        const scene = gltf.scene;
                        scene.userData = { pinData: pin };
                        this.scene.add(scene);
                        this.meshes.push({ scene: scene, transform: modelTransform, pinData: pin });
                    },
                    undefined,
                    (error) => {
                        console.warn('Could not load flag-marker.glb, using fallback cone:', error);
                        const fallbackMesh = new THREE.Mesh(geometry, material);
                        fallbackMesh.userData = { pinData: pin };
                        this.scene.add(fallbackMesh);
                        this.meshes.push({ scene: fallbackMesh, transform: modelTransform, pinData: pin });
                    }
                );
            });

            // Setup Raycaster
            this.raycaster = new THREE.Raycaster();
            this.mouse = new THREE.Vector2();

            map.on('click', (e) => this.handleRaycast(e));
        },

        handleRaycast: function (e) {
            // Need to handle raycasting in mapbox. 
            // Better to handle click events using mapbox's project, but 3D is tricky.
            // A simple approximation for click detection:
            let clickedPin = null;
            let minDistance = Infinity;

            this.meshes.forEach(m => {
                const screenPos = this.map.project([m.pinData.lng, m.pinData.lat]);
                const dx = screenPos.x - e.point.x;
                const dy = screenPos.y - e.point.y;
                const dist = Math.sqrt(dx * dx + dy * dy);

                // If within 20 pixels
                if (dist < 20 && dist < minDistance) {
                    minDistance = dist;
                    clickedPin = m.pinData;
                }
            });

            if (clickedPin) {
                // Determine popup HTML
                let content = `<div style='text-align:center;'>`;
                if (clickedPin.img) {
                    content += `<img src='${clickedPin.img}' alt='Find' class='popup-img'>`;
                }
                content += `<h4 style='margin:5px 0; color:var(--color-accent-primary);'>Community Find</h4>`;
                content += `<p style='margin:0; font-size:0.9rem;'>${clickedPin.desc}</p></div>`;

                new mapboxgl.Popup({ closeButton: true, closeOnClick: true, offset: 25 })
                    .setLngLat([clickedPin.lng, clickedPin.lat])
                    .setHTML(content)
                    .addTo(map);
            } else {
                // If not clicking a pin, ask if they want to add one
                openFindModal(e.lngLat.lng, e.lngLat.lat);
            }
        },

        render: function (gl, matrix) {
            const rotationX = new THREE.Matrix4().makeRotationAxis(
                new THREE.Vector3(1, 0, 0),
                0
            );
            const rotationY = new THREE.Matrix4().makeRotationAxis(
                new THREE.Vector3(0, 1, 0),
                0
            );
            const rotationZ = new THREE.Matrix4().makeRotationAxis(
                new THREE.Vector3(0, 0, 1),
                0
            );

            const m = new THREE.Matrix4().fromArray(matrix);
            const l = new THREE.Matrix4()
                .makeTranslation(
                    0, 0, 0
                )
                .scale(
                    new THREE.Vector3(1, 1, 1)
                )
                .multiply(rotationX)
                .multiply(rotationY)
                .multiply(rotationZ);

            this.camera.projectionMatrix = m.multiply(l);
            this.renderer.resetState();

            // Update positions of all meshes
            this.meshes.forEach(mObj => {
                const t = mObj.transform;
                mObj.scene.position.set(t.translateX, t.translateY, t.translateZ);
                mObj.scene.rotation.set(t.rotateX, t.rotateY, t.rotateZ);
                mObj.scene.scale.set(t.scale, t.scale, t.scale);
            });

            this.renderer.render(this.scene, this.camera);
            this.map.triggerRepaint();
        }
    };

    map.addLayer(customLayer, 'waterway-label');
}


/* ==========================
   MODAL & FORM LOGIC
   ========================== */
const findModal = document.getElementById('find-modal');
const closeFindBtn = document.getElementById('close-find-modal');
const findForm = document.getElementById('find-form');
const latInput = document.getElementById('find-lat');
const lngInput = document.getElementById('find-lng');

// Dropzone elements
const dropzone = document.getElementById('dropzone');
const photoInput = document.getElementById('find-photo');
const previewContainer = document.getElementById('preview-container');
const photoPreview = document.getElementById('photo-preview');

function openFindModal(lng, lat) {
    lngInput.value = lng;
    latInput.value = lat;
    findModal.showModal();
    findModal.style.display = 'flex';
}

closeFindBtn.addEventListener('click', () => {
    findModal.close();
    findModal.style.display = 'none';
    findForm.reset();
    previewContainer.style.display = 'none';
});

// Click outside to close
findModal.addEventListener('click', (e) => {
    if (e.target === findModal) {
        findModal.close();
        findModal.style.display = 'none';
        findForm.reset();
        previewContainer.style.display = 'none';
    }
});

// Dropzone interactions
dropzone.addEventListener('click', () => photoInput.click());

dropzone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropzone.classList.add('dragover');
});

dropzone.addEventListener('dragleave', () => {
    dropzone.classList.remove('dragover');
});

dropzone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropzone.classList.remove('dragover');
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
        photoInput.files = e.dataTransfer.files;
        handleFilePreview(photoInput.files[0]);
    }
});

photoInput.addEventListener('change', () => {
    if (photoInput.files && photoInput.files.length > 0) {
        handleFilePreview(photoInput.files[0]);
    }
});

function handleFilePreview(file) {
    if (file.type.startsWith('image/')) {
        const reader = new FileReader();
        reader.onload = (e) => {
            photoPreview.src = e.target.result;
            previewContainer.style.display = 'block';
            dropzone.querySelector('svg').style.display = 'none';
            dropzone.querySelector('p').style.display = 'none';
        };
        reader.readAsDataURL(file);
    }
}

// Form Submission
findForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const submitBtn = document.getElementById('submit-find-btn');
    const originalText = submitBtn.innerText;
    submitBtn.innerText = 'Uploading...';
    submitBtn.disabled = true;

    const formData = new FormData(findForm);

    try {
        const response = await fetch('save-pin.php', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();

        if (result.success) {
            alert('Your find has been posted!');
            findModal.close();
            findModal.style.display = 'none';
            findForm.reset();
            previewContainer.style.display = 'none';
            dropzone.querySelector('svg').style.display = 'block';
            dropzone.querySelector('p').style.display = 'block';

            // Reload the page to show the new pin
            window.location.reload();
        } else {
            alert('Error: ' + result.error);
        }
    } catch (err) {
        console.error(err);
        alert('An error occurred while posting your find.');
    } finally {
        submitBtn.innerText = originalText;
        submitBtn.disabled = false;
    }
});
