import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import './style.css';

// DOM elements
const container = document.querySelector('#app');
const loadingOverlay = document.querySelector('#loading-overlay');
const loadingProgress = document.querySelector('#loading-progress');
const lightDot = document.querySelector('#light-dot');
const lightStatusText = document.querySelector('#light-status-text');

// Scene, Camera, Renderer
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x111116);
scene.fog = new THREE.FogExp2(0x111116, 0.007);

const camera = new THREE.PerspectiveCamera(
  45,
  window.innerWidth / window.innerHeight,
  0.5,
  1500
);

const renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: 'high-performance' });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.15;
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
container.appendChild(renderer.domElement);

// Controls (Mouse Orbit support while Keyboard controls camera actively)
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.06;
controls.maxPolarAngle = Math.PI / 2 - 0.02; // keep above ground
controls.minDistance = 5;
controls.maxDistance = 250;

// Lighting for scene visibility (so train & platform textures are rendered beautifully)
// NOTE: These are static environment lights for scene illumination.
// The controlled light is the model's light material (Light_Texture) inside Station.glb!
const hemiLight = new THREE.HemisphereLight(0xddeeff, 0x161720, 1.4);
scene.add(hemiLight);

const mainSun = new THREE.DirectionalLight(0xfff5e6, 2.0);
mainSun.position.set(45, 90, 50);
mainSun.castShadow = true;
mainSun.shadow.mapSize.width = 2048;
mainSun.shadow.mapSize.height = 2048;
mainSun.shadow.bias = -0.0001;
scene.add(mainSun);

const fillLight = new THREE.DirectionalLight(0x7090b8, 0.8);
fillLight.position.set(-50, 40, -40);
scene.add(fillLight);

// Station & Train variables
let stationModel = null;
let trainGroup = null;
const lightMaterials = new Set();
let isLightOn = true;

// Exact list of 83 train nodes within Station.glb RootNode
const trainNodeNames = new Set([
  'Bacj wheel.001', 'Bacj wheel.002', 'Bacj wheel.003', 'Bacj wheel.004',
  'Bacj wheel.005', 'Bacj wheel.006', 'Bacj wheel.007', 'Bacj wheel.008',
  'Back door', 'Back door fluff.001', 'Back door fluff.002', 'Back door.001',
  'Back fluff', 'Back fluff.001',
  'Back lights.001', 'Back lights.003', 'Back lights.007',
  'Back panel', 'Back panel.001',
  'Back platform', 'Back platform.001',
  'Car back empty', 'Car body', 'Car body bottom', 'Car body bottom.001',
  'Car body bottom.002', 'Car body bottom.003', 'Car body bottom.004', 'Car body.001',
  'Door 1', 'Door 1.001', 'Door 2', 'Door 2.001',
  'Finale head lower', 'Finale head lower.001',
  'Front break', 'Front break attecher', 'Front break buffer',
  'Front lights', 'Front window side',
  'Top Exhaust 1', 'Top Exhaust 1.001', 'Top exhaiust 2', 'Top exhaiust 2.001',
  'Top generator', 'Top generator 2', 'Top generator 2.001', 'Top generator.001',
  'Top rails', 'Top rails.001', 'Top rails.002', 'Top rails.003',
  'Top rails.004', 'Top rails.005', 'Top rails.006', 'Top rails.007',
  'Tow arm', 'Tow arm.001', 'Tow clip', 'Tow clip.001',
  'Tow screw', 'Tow screw.001', 'Tow shaft', 'Tow shaft.001',
  'Train Head', 'Train Head.001', 'Train back gen', 'Train back gen.001',
  'Train lights front', 'Train lights front.001',
  'Train wheel main spring', 'Train wheel main spring.001', 'Train wheel main spring.002', 'Train wheel main spring.003',
  'Wheel main bracket', 'Wheel main bracket.001', 'Wheel main bracket.002', 'Wheel main bracket.003'
]);

// Build sanitized node names set to match Three.js GLTFLoader PropertyBinding sanitization
const sanitizedTrainNodeNames = new Set(
  Array.from(trainNodeNames).map((name) => THREE.PropertyBinding.sanitizeNodeName(name))
);

function isTrainNode(name) {
  if (!name) return false;
  return (
    trainNodeNames.has(name) ||
    sanitizedTrainNodeNames.has(name) ||
    sanitizedTrainNodeNames.has(THREE.PropertyBinding.sanitizeNodeName(name))
  );
}

// Light Control Function
// Controls the emissive property of the light in the model (Light_Texture material)
function setLightState(on) {
  isLightOn = on;
  lightMaterials.forEach(mat => {
    if (on) {
      mat.emissive.setRGB(1, 1, 1);
      mat.emissiveIntensity = mat.userData.originalEmissiveIntensity || 6;
    } else {
      mat.emissive.setRGB(0, 0, 0);
      mat.emissiveIntensity = 0;
    }
    mat.needsUpdate = true;
  });

  if (lightDot && lightStatusText) {
    if (on) {
      lightDot.classList.remove('off');
      lightStatusText.textContent = 'Train Light: ON';
    } else {
      lightDot.classList.add('off');
      lightStatusText.textContent = 'Train Light: OFF';
    }
  }
}

function toggleLight() {
  setLightState(!isLightOn);
}

// Load Station.glb
const loader = new GLTFLoader();
loader.load(
  '/models/Station.glb',
  (gltf) => {
    stationModel = gltf.scene;
    scene.add(stationModel);

    // Compute bounding box and center
    const box = new THREE.Box3().setFromObject(stationModel);
    const center = box.getCenter(new THREE.Vector3());
    const size = box.getSize(new THREE.Vector3());

    // Position camera for an isometric overview matching Image 3 (looking at the front-left of the train)
    // Front of train is at +Z, station waiting room is at -X, platform is at +X
    controls.target.set(center.x + 3.0, center.y + 1.5, center.z + 12.0);

    camera.position.set(
      center.x - 38.0,
      center.y + 28.0,
      center.z + 46.0
    );
    camera.lookAt(controls.target);
    controls.update();

    defaultTarget.copy(controls.target);
    defaultCameraPos.copy(camera.position);

    // Find RootNode and assemble the train group for animation
    let rootNode = null;
    stationModel.traverse((obj) => {
      if (obj.name === 'RootNode') rootNode = obj;
      
      // Collect light materials directly from the model
      if (obj.isMesh && obj.material) {
        const mats = Array.isArray(obj.material) ? obj.material : [obj.material];
        mats.forEach((mat) => {
          if (mat.name === 'Light_Texture' || (mat.emissive && (mat.emissive.r > 0 || mat.emissive.g > 0 || mat.emissive.b > 0))) {
            if (!mat.userData.originalEmissiveIntensity) {
              mat.userData.originalEmissiveIntensity = mat.emissiveIntensity || 6;
            }
            lightMaterials.add(mat);
          }
        });
        
        // Shadows
        obj.castShadow = true;
        obj.receiveShadow = true;
      }
    });

    if (rootNode) {
      trainGroup = new THREE.Group();
      trainGroup.name = 'TrainAnimatedGroup';
      rootNode.add(trainGroup);

      const childrenToMove = [];
      rootNode.children.forEach((child) => {
        if (child !== trainGroup && isTrainNode(child.name)) {
          childrenToMove.push(child);
        }
      });

      childrenToMove.forEach((child) => {
        trainGroup.add(child);
      });
      console.log(`Successfully grouped ${childrenToMove.length} train objects for animation.`);
    }

    // Initialize lights ON
    setLightState(true);

    // Hide loader
    if (loadingOverlay) {
      loadingOverlay.classList.add('hidden');
    }
  },
  (xhr) => {
    if (xhr.lengthComputable && loadingProgress) {
      const percent = Math.round((xhr.loaded / xhr.total) * 100);
      loadingProgress.textContent = `${percent}%`;
    }
  },
  (error) => {
    console.error('An error happened while loading Station.glb:', error);
    if (loadingProgress) {
      loadingProgress.textContent = 'Error loading 3D model';
    }
  }
);

// Mouse Interaction: Clicking toggles train light on/off
let pointerDownPos = new THREE.Vector2();
window.addEventListener('pointerdown', (e) => {
  pointerDownPos.set(e.clientX, e.clientY);
});

window.addEventListener('pointerup', (e) => {
  const dist = pointerDownPos.distanceTo(new THREE.Vector2(e.clientX, e.clientY));
  // If not dragged (pure click) and left button
  if (dist < 6 && e.button === 0) {
    toggleLight();
  }
});

// Keyboard Interaction: Camera will move around the train station
const activeKeys = {
  ArrowLeft: false,
  ArrowRight: false,
  ArrowUp: false,
  ArrowDown: false,
  KeyA: false,
  KeyD: false,
  KeyW: false,
  KeyS: false,
  KeyQ: false,
  KeyE: false
};

window.addEventListener('keydown', (e) => {
  if (e.code in activeKeys) {
    activeKeys[e.code] = true;
  }
  if (e.code === 'KeyR' && defaultCameraPos.lengthSq() > 0) {
    camera.position.copy(defaultCameraPos);
    controls.target.copy(defaultTarget);
    controls.update();
  }
});

window.addEventListener('keyup', (e) => {
  if (e.code in activeKeys) {
    activeKeys[e.code] = false;
  }
});

// Helper for orbiting camera around controls.target with keyboard
const offset = new THREE.Vector3();
const spherical = new THREE.Spherical();

function updateKeyboardCamera(dt) {
  const rotateSpeed = 1.35; // radians per second
  const zoomSpeed = 28.0;   // units per second
  const elevSpeed = 15.0;   // height units per second

  let changed = false;

  offset.copy(camera.position).sub(controls.target);
  spherical.setFromVector3(offset);

  // Left / Right: Orbit around the train station
  if (activeKeys.ArrowLeft || activeKeys.KeyA) {
    spherical.theta -= rotateSpeed * dt;
    changed = true;
  }
  if (activeKeys.ArrowRight || activeKeys.KeyD) {
    spherical.theta += rotateSpeed * dt;
    changed = true;
  }

  // Up / Down: Move closer / further (zoom along ray)
  if (activeKeys.ArrowUp || activeKeys.KeyW) {
    spherical.radius = Math.max(controls.minDistance, spherical.radius - zoomSpeed * dt);
    changed = true;
  }
  if (activeKeys.ArrowDown || activeKeys.KeyS) {
    spherical.radius = Math.min(controls.maxDistance, spherical.radius + zoomSpeed * dt);
    changed = true;
  }

  // Q / E: Elevation (pitch up / down)
  if (activeKeys.KeyQ) {
    spherical.phi = Math.max(0.12, spherical.phi - (rotateSpeed * 0.6) * dt);
    changed = true;
  }
  if (activeKeys.KeyE) {
    spherical.phi = Math.min(controls.maxPolarAngle, spherical.phi + (rotateSpeed * 0.6) * dt);
    changed = true;
  }

  if (changed) {
    offset.setFromSpherical(spherical);
    camera.position.copy(controls.target).add(offset);
  }
}

// Default camera and target for reset (KeyR)
const defaultCameraPos = new THREE.Vector3();
const defaultTarget = new THREE.Vector3();

// Animation: Train will move in and out of the station
// 1. Train stopped at station platform (DWELL)
// 2. Train accelerates smoothly forward along track out of station (DEPART)
// 3. Train briefly clears station in distance (AWAY)
// 4. Train appears on approach track, glides into station and smoothly brakes to a stop at platform (ARRIVE)
// Animation: Train will move in and out of the station
// 1. Train arrives into station and smoothly brakes to a stop at platform (ARRIVE: 6s)
// 2. Train stopped at station platform for passengers (DWELL: 4.5s)
// 3. Train accelerates smoothly forward along track out of station (DEPART: 5.5s)
// 4. Train outside station on approach track (AWAY: 1.5s)
// Total loop: 17.5s

let trainCycleTime = 1.0; // Start with train actively arriving into the station
const ARRIVE_TIME = 6.0;    // Entering station and braking to stop (seconds)
const DWELL_TIME = 4.5;     // Stopped at station platform (seconds)
const DEPART_TIME = 5.5;    // Accelerating and moving out of station (seconds)
const AWAY_TIME = 1.5;      // Outside station interval (seconds)
const TOTAL_CYCLE = ARRIVE_TIME + DWELL_TIME + DEPART_TIME + AWAY_TIME; // 17.5s loop

const MAX_DEPART_Z = 8500;  // Outside station along +Z
const MIN_ENTER_Z = -8500;  // Approach track along -Z
const trainStatusText = document.querySelector('#train-status-text');

function updateTrainMovement(dt) {
  if (!trainGroup) return;

  trainCycleTime += dt;
  const normTime = trainCycleTime % TOTAL_CYCLE;

  // Phase 1: Arriving - smoothly entering station along tracks and braking to a stop
  if (normTime < ARRIVE_TIME) {
    trainGroup.visible = true;
    const arriveProgress = normTime / ARRIVE_TIME;
    // Smooth ease-out deceleration to stop at platform (z = 0)
    const eased = Math.sin((arriveProgress * Math.PI) / 2);
    trainGroup.position.z = MIN_ENTER_Z * (1 - eased);

    if (trainStatusText) {
      trainStatusText.textContent = 'Train: Arriving at Station...';
      trainStatusText.style.color = '#38bdf8';
    }
    return;
  }

  // Phase 2: Stopped at station platform (Dwell / Boarding)
  const dwellEnd = ARRIVE_TIME + DWELL_TIME;
  if (normTime < dwellEnd) {
    trainGroup.visible = true;
    trainGroup.position.z = 0;

    if (trainStatusText) {
      trainStatusText.textContent = 'Train: At Platform (Stopped)';
      trainStatusText.style.color = '#4ade80';
    }
    return;
  }

  // Phase 3: Departing - smoothly accelerating out of station along tracks
  const departEnd = dwellEnd + DEPART_TIME;
  if (normTime < departEnd) {
    trainGroup.visible = true;
    const progress = (normTime - dwellEnd) / DEPART_TIME;
    // Smooth ease-in acceleration
    const eased = 1 - Math.cos((progress * Math.PI) / 2);
    trainGroup.position.z = eased * MAX_DEPART_Z;

    if (trainStatusText) {
      trainStatusText.textContent = 'Train: Departing Station...';
      trainStatusText.style.color = '#fbbf24';
    }
    return;
  }

  // Phase 4: Away - outside station in distance
  trainGroup.visible = false;
  trainGroup.position.z = MIN_ENTER_Z;

  if (trainStatusText) {
    trainStatusText.textContent = 'Train: Approaching Station...';
    trainStatusText.style.color = '#94a3b8';
  }
}

// Render Loop
const clock = new THREE.Clock();

function animate() {
  requestAnimationFrame(animate);

  const dt = Math.min(clock.getDelta(), 0.1);

  // Update keyboard camera movement
  updateKeyboardCamera(dt);

  // Update OrbitControls
  controls.update();

  // Update Train Animation ("Train will move in and out of the station")
  updateTrainMovement(dt);

  renderer.render(scene, camera);
}

animate();

// Responsive Resize
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
});
