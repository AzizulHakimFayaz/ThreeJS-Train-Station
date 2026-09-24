import os
import reportlab
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image as RLImage, Table, TableStyle, PageBreak, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch

def create_report():
    pdf_path = "Project_Final_Report_Train_Station.pdf"
    
    # 0.75 in (54 pt) margins on A4 (595.27 x 841.89 pt) -> usable width = 487.27 pt, usable height = 733.89 pt
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    
    # Custom Typography matching the sample PDF
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=28,
        leading=34,
        alignment=1, # Center
        spaceAfter=14
    )
    
    course_style = ParagraphStyle(
        'CoverCourse',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=20,
        alignment=1,
        spaceAfter=6
    )
    
    report_type_style = ParagraphStyle(
        'CoverReportType',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=13,
        leading=18,
        alignment=1,
        spaceAfter=24
    )
    
    meta_style = ParagraphStyle(
        'CoverMeta',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=16,
        alignment=1,
        spaceAfter=4
    )
    
    heading1_style = ParagraphStyle(
        'SectionHeading',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=18,
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )
    
    heading2_style = ParagraphStyle(
        'SubSectionHeading',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        spaceBefore=10,
        spaceAfter=6,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'ReportBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        spaceAfter=6
    )
    
    bullet_style = ParagraphStyle(
        'ReportBullet',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        leftIndent=14,
        firstLineIndent=-10,
        spaceAfter=3
    )
    
    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=colors.black
    )
    
    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5
    )
    
    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11.5
    )
    
    caption_style = ParagraphStyle(
        'FigureCaption',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9,
        leading=13,
        alignment=1, # Center
        spaceBefore=5,
        spaceAfter=15
    )

    live_url_style = ParagraphStyle(
        'LiveURL',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=15,
        spaceBefore=10,
        spaceAfter=15
    )

    story = []
    
    # -------------------------------------------------------------
    # PAGE 1: COVER PAGE
    # -------------------------------------------------------------
    story.append(Spacer(1, 40))
    if os.path.exists('report_assets/seu_logo.png'):
        # Logo centered
        logo_img = RLImage('report_assets/seu_logo.png', width=110, height=110)
        logo_img.hAlign = 'CENTER'
        story.append(logo_img)
    story.append(Spacer(1, 45))
    
    story.append(Paragraph("A Train Station", title_style))
    story.append(Paragraph("Computer Graphics &amp; Animation Lab (CSE 444)", course_style))
    story.append(Paragraph("Project Final Report", report_type_style))
    story.append(Spacer(1, 15))
    
    story.append(Paragraph("Section: 7", meta_style))
    story.append(Paragraph("Group No.: 09", meta_style))
    story.append(Paragraph("Assigned Project No.: 20", meta_style))
    story.append(Spacer(1, 45))
    
    # Submitted By Table
    submitted_data = [
        [Paragraph("Submitted By:", table_cell_bold), ""],
        [Paragraph("Azizul Hakim Fayaz", table_cell_style), Paragraph("2023100010209", table_cell_style)],
        [Paragraph("Jakaria Kabir Provat", table_cell_style), Paragraph("2023100010203", table_cell_style)],
        [Paragraph("Shourov Sarkar", table_cell_style), Paragraph("2023100010093", table_cell_style)]
    ]
    t_submit = Table(submitted_data, colWidths=[200, 160])
    t_submit.setStyle(TableStyle([
        ('SPAN', (0, 0), (1, 0)),
        ('BACKGROUND', (0, 0), (1, 0), colors.white),
        ('BOX', (0, 0), (-1, -1), 0.8, colors.black),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    t_submit.hAlign = 'CENTER'
    story.append(t_submit)
    
    story.append(PageBreak())
    
    # -------------------------------------------------------------
    # PAGE 2: REQUIREMENTS, SOFTWARE PLATFORM, & FEATURES (3.1)
    # -------------------------------------------------------------
    story.append(Paragraph("1. Project Requirements", heading1_style))
    story.append(Paragraph(
        "The primary goal of this project is to render an interactive 3D train station scene centered on a passenger train, station platform, tracks, and waiting facilities using Three.js. The project must fulfil the following general requirements: 3D model loading and texture mapping, lighting, perspective projection, realistic shadows, multi-stage animation, and mouse and keyboard interaction.",
        body_style
    ))
    story.append(Paragraph("Project-specific requirements:", body_style))
    story.append(Paragraph("• A detailed 3D train station with platform, waiting building, track sleepers, passenger benches, and overhead canopies.", bullet_style))
    story.append(Paragraph("• A passenger train consisting of locomotive engine and passenger wagons with realistic textures.", bullet_style))
    story.append(Paragraph("• The camera can move around the train station using both mouse orbiting and keyboard navigation.", bullet_style))
    story.append(Paragraph("• Train headlight and cabin lights toggle ON and OFF at runtime via mouse click with visual emissive feedback.", bullet_style))
    story.append(Paragraph("• Multi-stage train motion animation: the train arrives, decelerates smoothly to halt at the platform for boarding, and departs along the tracks.", bullet_style))
    story.append(Paragraph("• Real-time on-screen HUD displaying status indicators and interactive controls.", bullet_style))
    
    story.append(Spacer(1, 4))
    story.append(Paragraph("2. Software Platform", heading1_style))
    platform_data = [
        [Paragraph("Tool / Technology", table_header_style), Paragraph("Purpose", table_header_style)],
        [Paragraph("Three.js (v0.186)", table_cell_bold), Paragraph("3D rendering library built on WebGL", table_cell_style)],
        [Paragraph("JavaScript (ES modules)", table_cell_bold), Paragraph("Scene logic, animation, keyboard/mouse interaction and event handling", table_cell_style)],
        [Paragraph("GLTFLoader", table_cell_bold), Paragraph("Loading high-fidelity 3D glTF/GLB models (Station.glb, Engine.glb, wagon.glb)", table_cell_style)],
        [Paragraph("OrbitControls", table_cell_bold), Paragraph("Interactive camera orbiting, damping, rotation, and distance clamping", table_cell_style)],
        [Paragraph("HTML5 / CSS3", table_cell_bold), Paragraph("HUD overlay, status badges, instructions card, and responsive canvas layout", table_cell_style)],
        [Paragraph("Vite (v8.3)", table_cell_bold), Paragraph("Development server and high-speed production module bundler", table_cell_style)],
        [Paragraph("Netlify", table_cell_bold), Paragraph("Continuous deployment (CI/CD) and cloud web hosting", table_cell_style)],
        [Paragraph("Node.js / npm", table_cell_bold), Paragraph("Package management and build scripts", table_cell_style)],
        [Paragraph("Visual Studio Code", table_cell_bold), Paragraph("Source code editor and development environment", table_cell_style)]
    ]
    t_platform = Table(platform_data, colWidths=[140, 347])
    t_platform.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#dce2f4')),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#444444')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#444444')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    t_platform.hAlign = 'LEFT'
    story.append(t_platform)
    
    story.append(Spacer(1, 6))
    story.append(Paragraph("3. Project Features", heading1_style))
    story.append(Paragraph("3.1 Models and Texture Mapping", heading2_style))
    story.append(Paragraph(
        "All 3D models are structured into optimized glTF/GLB assets and loaded asynchronously into the Three.js scene graph. The station environment contains intricate meshes for the station shelter, roofing, corrugated iron sheets, platforms, tracks, waste bins, platform lights, and benches. Every object incorporates physically-based materials (PBR) with diffuse, roughness, metalness, and emissive properties.",
        body_style
    ))
    
    models_part1 = [
        [Paragraph("Object", table_header_style), Paragraph("Geometry", table_header_style), Paragraph("Texture and reason", table_header_style)],
        [
            Paragraph("Train Locomotive", table_cell_bold),
            Paragraph("Aerodynamic cab shell, bogies, front buffers, cowcatcher, dual headlights", table_cell_style),
            Paragraph("PBR metallic blue and yellow paint textures, emissive headlight glass, glossy window panels.", table_cell_style)
        ],
        [
            Paragraph("Passenger Wagons", table_cell_bold),
            Paragraph("Articulated carriages, windows, bogies, suspension springs, and doors", table_cell_style),
            Paragraph("Deep blue coach livery texture, glass windows, industrial steel roof texture.", table_cell_style)
        ]
    ]
    t_models1 = Table(models_part1, colWidths=[95, 155, 237])
    t_models1.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#dce2f4')),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#444444')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#444444')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    t_models1.hAlign = 'LEFT'
    story.append(t_models1)
    
    story.append(PageBreak())
    
    # -------------------------------------------------------------
    # PAGE 3: MODELS CONTINUED & 3.2 KEY INTERACTION
    # -------------------------------------------------------------
    models_part2 = [
        [Paragraph("Object", table_header_style), Paragraph("Geometry", table_header_style), Paragraph("Texture and reason", table_header_style)],
        [
            Paragraph("Station Platform &amp; Canopy", table_cell_bold),
            Paragraph("Reinforced concrete platforms, textured tiles, corrugated roof panels", table_cell_style),
            Paragraph("Weathered corrugated metal texture with rust accents, concrete slab diffuse map with yellow safety edge lines.", table_cell_style)
        ],
        [
            Paragraph("Railway Tracks", table_cell_bold),
            Paragraph("Steel parallel rails, wooden sleepers/ties, ballast gravel base", table_cell_style),
            Paragraph("Ballast stone texture and rustic weathered steel rails for realistic physical track representation.", table_cell_style)
        ],
        [
            Paragraph("Platform Amenities", table_cell_bold),
            Paragraph("Benches, trash receptacles, informational boards, light poles", table_cell_style),
            Paragraph("Powder-coated metal textures, glass panels, and plastic materials for authentic depot environment.", table_cell_style)
        ]
    ]
    t_models2 = Table(models_part2, colWidths=[95, 155, 237])
    t_models2.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#dce2f4')),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#444444')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#444444')),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    t_models2.hAlign = 'LEFT'
    story.append(t_models2)
    
    story.append(Spacer(1, 14))
    story.append(Paragraph("3.2 Key Interaction", heading1_style))
    story.append(Paragraph(
        "Keyboard events are handled with keydown and keyup listeners tracking active keys in a state map. The camera orbits around a central focus point on the station. The arrow keys (or WASD keys) dynamically modify the spherical coordinates (theta for azimuth angle, phi for polar angle, and radius for zoom distance) relative to the target vector. The updated camera position vector is calculated in real time using Three.js Spherical.setFromVector3() and setFromSpherical(). Left/Right rotate the camera horizontally around the station, Up/Down zoom along the view ray, and Q/E adjust the elevation angle. The polar angle is clamped so the camera never clips through the ground. Key 'R' resets the camera position and focus target to the initial isometric overview.",
        body_style
    ))
    
    key_data = [
        [Paragraph("Key", table_header_style), Paragraph("Action", table_header_style)],
        [Paragraph("Left / Right Arrow (or A / D)", table_cell_bold), Paragraph("Rotate / orbit camera horizontally around the station", table_cell_style)],
        [Paragraph("Up / Down Arrow (or W / S)", table_cell_bold), Paragraph("Move camera closer or farther (zoom in / zoom out along view ray)", table_cell_style)],
        [Paragraph("Q / E", table_cell_bold), Paragraph("Tilt camera elevation up or down (pitch angle)", table_cell_style)],
        [Paragraph("R", table_cell_bold), Paragraph("Reset camera view and target back to the initial isometric overview", table_cell_style)]
    ]
    t_keys = Table(key_data, colWidths=[150, 337])
    t_keys.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#dce2f4')),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#444444')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#444444')),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    t_keys.hAlign = 'LEFT'
    story.append(t_keys)
    
    story.append(PageBreak())
    
    # -------------------------------------------------------------
    # PAGE 4: MOUSE INTERACTION, ANIMATION, LIGHTING, SHADERS
    # -------------------------------------------------------------
    story.append(Paragraph("3.3 Mouse Interaction", heading1_style))
    story.append(Paragraph("• Left-button drag: Rotates and orbits the camera around the station target using Three.js OrbitControls with smooth damping.", bullet_style))
    story.append(Paragraph("• Mouse wheel: Zooms in and out smoothly within a bounded distance range (min: 5, max: 250 units).", bullet_style))
    story.append(Paragraph("• Click on canvas: Toggles the train's headlights and cabin lights ON and OFF. A click is separated from a drag operation by checking that the pointer moved less than 6 pixels between pointerdown and pointerup, preventing accidental light toggles during scene rotation.", bullet_style))
    
    story.append(Spacer(1, 6))
    story.append(Paragraph("3.4 Animation", heading1_style))
    story.append(Paragraph("• Cyclic Train Movement: The train's motion is driven by an elapsed cycle clock (total loop: 17.5s) divided into four smooth phases:", bullet_style))
    story.append(Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;1. Arrive Phase (6.0s): Train enters the station along the tracks, applying smooth sinusoidal ease-out deceleration (Math.sin(progress * PI / 2)) until coming to a complete stop at the platform.", bullet_style))
    story.append(Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;2. Dwell Phase (4.5s): Train remains stationary at the passenger platform (position.z = 0) allowing passenger boarding, while HUD displays 'Train: At Platform (Stopped)'.", bullet_style))
    story.append(Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;3. Depart Phase (5.5s): Train smoothly accelerates away along the track out of the station using sinusoidal ease-in acceleration (1 - Math.cos(progress * PI / 2)).", bullet_style))
    story.append(Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;4. Away Phase (1.5s): Train resets position along the approach track outside the station.", bullet_style))
    story.append(Paragraph("• Camera Motion Damping: Camera movement and rotation are smoothly interpolated each frame with damping for fluid, cinematic navigation.", bullet_style))
    story.append(Paragraph("• RequestAnimationFrame Loop: All animations execute inside a requestAnimationFrame render loop using Three.js Clock.getDelta(), ensuring uniform speed across different monitor refresh rates.", bullet_style))
    
    story.append(Spacer(1, 6))
    story.append(Paragraph("3.5 Lighting", heading1_style))
    story.append(Paragraph(
        "Three lighting types are combined, and the Three.js MeshStandardMaterial uses a physically-based (PBR) lighting model where surface rendering depends on normals, lighting angles, roughness, and metalness:",
        body_style
    ))
    story.append(Paragraph("• Directional Light (Sun): Warm directional sunlight (0xfff5e6, intensity: 2.0) positioned at (45, 90, 50) casting realistic shadows across station roofs, platforms, and tracks using a 2048x2048 shadow map.", bullet_style))
    story.append(Paragraph("• Hemisphere Light: Ambient sky-to-ground light (0xddeeff sky, 0x161720 ground, intensity: 1.4) that illuminates shadowed areas and prevents black pitch-black voids.", bullet_style))
    story.append(Paragraph("• Fill Directional Light: Cool secondary directional light (0x7090b8, intensity: 0.8) positioned at (-50, 40, -40) providing complementary architectural depth.", bullet_style))
    story.append(Paragraph("• Emissive Train Headlights: Dynamic emissive material (Light_Texture) with intensity 6.0 creating vibrant train headlights.", bullet_style))
    story.append(Paragraph("Shadows are enabled with PCFSoftShadowMap for realistic soft edges, and ACESFilmicToneMapping ensures bright areas avoid harsh over-exposure.", body_style))
    
    story.append(Spacer(1, 6))
    story.append(Paragraph("3.6 Custom Shaders and Material Control", heading1_style))
    story.append(Paragraph(
        "Scene graph traversal automatically locates all light meshes and Light_Texture materials, caching their original emissive intensities. When toggled, the materials dynamically switch RGB values and emissive intensities between active and inactive states.",
        body_style
    ))
    
    story.append(PageBreak())
    
    # -------------------------------------------------------------
    # PAGE 5: SHADERS CONT. & TABLE 01: PROJECT FEATURE TABLE
    # -------------------------------------------------------------
    story.append(Paragraph(
        "• Material Uniforms & State: The Light_Texture material uses dynamic emissive properties. When activated, emissive intensity is boosted to 6.0 with pure white RGB (1, 1, 1). When deactivated, RGB is set to (0, 0, 0) with zero intensity, giving a realistic power-off appearance.<br/>"
        "• Atmospheric Depth: Configured with THREE.FogExp2 and dark charcoal clear color (0x111116) to seamlessly blend distant tracks and geometry into the horizon.<br/>"
        "• High Performance: Configured with powerPreference: 'high-performance' and device pixel ratio clamped to 2.0 for smooth 60fps rendering across desktop and mobile devices.",
        body_style
    ))
    story.append(Spacer(1, 8))
    
    story.append(Paragraph("Table 01: Project Feature Table", heading1_style))
    feature_data = [
        [Paragraph("#", table_header_style), Paragraph("Features", table_header_style), Paragraph("Status", table_header_style)],
        [Paragraph("1", table_cell_style), Paragraph("3D Train Station Scene with Platform &amp; Architecture", table_cell_style), Paragraph("Implemented", table_cell_bold)],
        [Paragraph("2", table_cell_style), Paragraph("Realistic Passenger Train (Locomotive &amp; Wagons)", table_cell_style), Paragraph("Implemented", table_cell_bold)],
        [Paragraph("3", table_cell_style), Paragraph("Realistic PBR Materials &amp; High-Res Textures", table_cell_style), Paragraph("Implemented", table_cell_bold)],
        [Paragraph("4", table_cell_style), Paragraph("Directional Sunlight &amp; Hemisphere Lighting", table_cell_style), Paragraph("Implemented", table_cell_bold)],
        [Paragraph("5", table_cell_style), Paragraph("Soft Shadow Mapping (PCFSoftShadowMap)", table_cell_style), Paragraph("Implemented", table_cell_bold)],
        [Paragraph("6", table_cell_style), Paragraph("Perspective Projection (PerspectiveCamera)", table_cell_style), Paragraph("Implemented", table_cell_bold)],
        [Paragraph("7", table_cell_style), Paragraph("Multi-Phase Train Arrival &amp; Departure Animation", table_cell_style), Paragraph("Implemented", table_cell_bold)],
        [Paragraph("8", table_cell_style), Paragraph("Train Headlights Emissive Light Toggle", table_cell_style), Paragraph("Implemented", table_cell_bold)],
        [Paragraph("9", table_cell_style), Paragraph("Keyboard Navigation (WASD / Arrow Keys Orbit &amp; Zoom)", table_cell_style), Paragraph("Implemented", table_cell_bold)],
        [Paragraph("10", table_cell_style), Paragraph("Mouse Interaction (OrbitControls &amp; Click Detection)", table_cell_style), Paragraph("Implemented", table_cell_bold)],
        [Paragraph("11", table_cell_style), Paragraph("Interactive HUD with Real-time Status Badges", table_cell_style), Paragraph("Implemented", table_cell_bold)],
        [Paragraph("12", table_cell_style), Paragraph("View Reset Functionality (Key 'R')", table_cell_style), Paragraph("Implemented", table_cell_bold)],
        [Paragraph("13", table_cell_style), Paragraph("Responsive WebGL Canvas &amp; ACES Filmic Tone Mapping", table_cell_style), Paragraph("Implemented", table_cell_bold)],
        [Paragraph("14", table_cell_style), Paragraph("Automated Netlify CI/CD Deployment", table_cell_style), Paragraph("Implemented", table_cell_bold)],
        [Paragraph("15", table_cell_style), Paragraph("Procedural Ambient Particles (Fog &amp; Smoke)", table_cell_style), Paragraph("Partially Implemented", table_cell_style)],
        [Paragraph("16", table_cell_style), Paragraph("Multi-Track Switching Logic", table_cell_style), Paragraph("Not Implemented", table_cell_style)],
    ]
    t_features = Table(feature_data, colWidths=[25, 345, 117])
    t_features.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#dce2f4')),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#444444')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#444444')),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    t_features.hAlign = 'LEFT'
    story.append(t_features)
    
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "Note: The camera was intentionally designed with both mouse and keyboard orbit capabilities, allowing complete interactive exploration of the train station platform, rails, and locomotive details.",
        body_style
    ))
    
    story.append(PageBreak())
    
    # -------------------------------------------------------------
    # PAGE 6: SNAPSHOTS (FIG 1 & FIG 2)
    # -------------------------------------------------------------
    story.append(Paragraph("4. Snapshots", heading1_style))
    story.append(Spacer(1, 10))
    
    if os.path.exists('report_assets/fig1_overview.png'):
        f1 = RLImage('report_assets/fig1_overview.png', width=450, height=222)
        f1.hAlign = 'CENTER'
        story.append(f1)
        story.append(Paragraph("Figure 1: Full scene overview (station, tracks, train, waiting building, platform)", caption_style))
        story.append(Spacer(1, 12))
        
    if os.path.exists('report_assets/fig2_stopped.png'):
        f2 = RLImage('report_assets/fig2_stopped.png', width=450, height=222)
        f2.hAlign = 'CENTER'
        story.append(f2)
        story.append(Paragraph("Figure 2: Train stopped at platform with passenger cars and station benches", caption_style))
        
    story.append(PageBreak())
    
    # -------------------------------------------------------------
    # PAGE 7: SNAPSHOTS (FIG 3 & FIG 4)
    # -------------------------------------------------------------
    story.append(Spacer(1, 15))
    if os.path.exists('report_assets/fig3_train_closeup.png'):
        f3 = RLImage('report_assets/fig3_train_closeup.png', width=450, height=209)
        f3.hAlign = 'CENTER'
        story.append(f3)
        story.append(Paragraph("Figure 3: Close-up of passenger train arriving at the platform", caption_style))
        story.append(Spacer(1, 20))
        
    if os.path.exists('report_assets/fig4_light_on.png'):
        f4 = RLImage('report_assets/fig4_light_on.png', width=450, height=227)
        f4.hAlign = 'CENTER'
        story.append(f4)
        story.append(Paragraph("Figure 4: Train headlights and cabin illumination ON (Emissive state: ON)", caption_style))
        
    story.append(PageBreak())
    
    # -------------------------------------------------------------
    # PAGE 8: SNAPSHOTS (FIG 5 & FIG 6)
    # -------------------------------------------------------------
    story.append(Spacer(1, 15))
    if os.path.exists('report_assets/fig5_light_off.png'):
        f5 = RLImage('report_assets/fig5_light_off.png', width=420, height=232)
        f5.hAlign = 'CENTER'
        story.append(f5)
        story.append(Paragraph("Figure 5: Train headlights toggled OFF via interactive mouse click", caption_style))
        story.append(Spacer(1, 20))
        
    if os.path.exists('report_assets/fig6_platform_architecture.png'):
        f6 = RLImage('report_assets/fig6_platform_architecture.png', width=450, height=222)
        f6.hAlign = 'CENTER'
        story.append(f6)
        story.append(Paragraph("Figure 6: Detailed view of station platform canopy, track sleepers, and architectural assets", caption_style))
        
    story.append(PageBreak())
    
    # -------------------------------------------------------------
    # PAGE 9: SNAPSHOT (FIG 7), LIVE URL, & CONTRIBUTION
    # -------------------------------------------------------------
    story.append(Spacer(1, 10))
    if os.path.exists('report_assets/fig7_track_angle.png'):
        f7 = RLImage('report_assets/fig7_track_angle.png', width=450, height=215)
        f7.hAlign = 'CENTER'
        story.append(f7)
        story.append(Paragraph("Figure 7: Camera rotated to view track layout and platform structure", caption_style))
        story.append(Spacer(1, 15))
        
    story.append(Paragraph("<b>Project Live URL:</b> <font color='#2563eb'><u>https://threejs-train-station.netlify.app/</u></font>", live_url_style))
    story.append(Paragraph("<b>GitHub Repository:</b> <font color='#2563eb'><u>https://github.com/AzizulHakimFayaz/ThreeJS-Train-Station</u></font>", ParagraphStyle('GitURL', parent=live_url_style, fontSize=9.5, leading=14, spaceBefore=0, spaceAfter=14)))
    story.append(Spacer(1, 4))
    
    story.append(Paragraph("5. Contribution", heading1_style))
    contribution_data = [
        [Paragraph("Member", table_header_style), Paragraph("Contribution", table_header_style)],
        [
            Paragraph("Azizul Hakim Fayaz<br/>(2023100010209)", table_cell_bold),
            Paragraph("3D Scene setup, GLTF model integration, lighting configuration, train grouping and hierarchical animation.", table_cell_style)
        ],
        [
            Paragraph("Jakaria Kabir Provat<br/>(2023100010203)", table_cell_bold),
            Paragraph("Keyboard and mouse camera controls, OrbitControls integration, camera reset system, and light toggle logic.", table_cell_style)
        ],
        [
            Paragraph("Shourov Sarkar<br/>(2023100010093)", table_cell_bold),
            Paragraph("UI/HUD styling, status indicators, shadow mapping optimization, project report documentation, and Netlify deployment.", table_cell_style)
        ]
    ]
    t_contrib = Table(contribution_data, colWidths=[150, 337])
    t_contrib.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#dce2f4')),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#444444')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#444444')),
        ('TOPPADDING', (0, 0), (-1, -1), 7),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    t_contrib.hAlign = 'LEFT'
    story.append(t_contrib)
    
    doc.build(story)
    print("Report PDF generated successfully:", pdf_path)

if __name__ == '__main__':
    create_report()
