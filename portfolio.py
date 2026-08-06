import streamlit as st
import datetime as date
import base64
import json
import textwrap
from pathlib import Path

st.set_page_config(
    page_title="Portfolio",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for beige and white aesthetic with dark brown text
st.markdown("""
<style>
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }

    body {
        background: #0a0705;
        color: #C5C3B9;
        font-family: Arial, monospace;
        line-height: 1.6;
    }

    .main {
        background-color: #0a0705;
    }

    .navbar {
        background: linear-gradient(90deg, #0a0705 0%, #771F02 100%);
        padding: 1rem 1rem;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.4);
    }

    .hero-section {
        background: linear-gradient(135deg, #0a0705 0%, #771F02 100%);
        padding: 2rem 1rem;
        text-align: center;
        border-radius: 10px;
        margin-bottom: 3rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
    }

    .hero-section h1 {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        color: #C5C3B9;
        text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.5);
    }

    .hero-section p {
        font-size: 1.3rem;
        opacity: 0.95;
        margin-bottom: 1.5rem;
    }

    .social-links {
        display: flex;
        justify-content: center;
        gap: 1.5rem;
        margin-top: 1.5rem;
        flex-wrap: wrap;
    }

    .social-btn {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.75rem 1.5rem;
        background-color: #771F02;
        color: #C5C3B9;
        text-decoration: none;
        border-radius: 5px;
        transition: all 0.3s ease;
        border: 2px solid #771F02;
        font-weight: 500;
    }

    .social-btn:hover {
        background-color: #FC801D;
        border-color: #b88153;
        transform: translateY(-5px);
        box-shadow: 0 5px 15px #FC801D;
    }

    .social-icon-btn {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 50px;
        height: 50px;
        background-color: #771F02;
        border-radius: 8px;
        transition: all 0.3s ease;
        border: 2px solid #771F02;
        cursor: pointer;
        text-decoration: none;
    }

    .social-icon-btn img {
        width: 28px;
        height: 28px;
        display: block;
    }

    .social-icon-btn:hover {
        background-color: #FC801D;
        border-color: #b88153;
        transform: translateY(-5px);
        box-shadow: 0 5px 15px #FC801D;
    }

    /* Style Streamlit download button to match .social-btn */
    [data-testid="stDownloadButton"] > button,
    [data-testid="stDownloadButton"] button {
        display: inline-flex !important;
        align-items: center !important;
        gap: 0.5rem !important;
        padding: 0.75rem 1.5rem !important;
        background-color: #771F02 !important;
        color: #C5C3B9 !important;
        text-decoration: none !important;
        border-radius: 5px !important;
        transition: all 0.3s ease !important;
        border: 2px solid #771F02 !important;
        font-weight: 500 !important;
        box-shadow: none !important;
    }

    [data-testid="stDownloadButton"] > button:hover,
    [data-testid="stDownloadButton"] button:hover {
        background-color: #FC801D !important;
        border-color: #b88153 !important;
        transform: translateY(-5px) !important;
        box-shadow: 0 5px 15px #FC801D !important;
        cursor: pointer !important;
    }

    [data-testid="stTabs"] [data-baseweb="tab-list"] {
        gap: 0.35rem;
        border-bottom: 1px solid rgba(119, 31, 2, 0.45);
    }

    [data-testid="stTabs"] [data-baseweb="tab-highlight"] {
        background-color: transparent !important;
    }

    [data-testid="stTabs"] button[role="tab"] {
        background: transparent;
        color: #C5C3B9;
        border: 1px solid rgba(119, 31, 2, 0.7);
        border-radius: 999px;
        padding: 0.75rem 1rem;
        min-height: 2.4rem;
        line-height: 1.2;
        transition: background-color 0.2s ease, color 0.2s ease, box-shadow 0.2s ease, transform 0.2s ease;
    }

    [data-testid="stTabs"] button[role="tab"]:hover {
        background: rgba(119, 31, 2, 0.12);
        box-shadow: 0 0 0 1px rgba(119, 31, 2, 0.3);
        transform: translateY(-1px);
    }

    [data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
        background: #771F02;
        color: #C5C3B9;
        box-shadow: 0 0 0 1px rgba(197, 195, 185, 0.14);
    }

    .section-title {
        color: #C5C3B9;
        font-size: 2rem;
        font-weight: 700;
        margin: 3rem 0 3rem 0;
        padding-bottom: 1rem;
    }

    .project-card {
        background: #0a0705;
        border-radius: 10px;
        padding: 2rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 15px #771F02;
        transition: all 0.3s ease;
    }

    .project-card:hover {
        box-shadow: 0 8px 25px #771F02;
        transform: translateY(-5px);
    }

    .project-card h3 {
        color: #C5C3B9;
        font-size: 1.5rem;
        margin-bottom: 0.5rem;
    }

    .project-card .tags {
        margin-top: 1rem;
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        margin-bottom: 1rem;
    }

    .tag {
        background-color: #0a0705;
        color: #C5C3B9;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 500;
    }

    .skills-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1.5rem;
        margin-bottom: 2rem;
    }

    .skill-category {
        background-color: #0a0705;
        border-radius: 8px;
        padding: 1.5rem;
        box-shadow: 0 4px 15px #C5C3B9;
        border-top: 4px solid #771F02;
    }

    .skill-category h4 {
        color: #771F02;
        padding: 0.5rem 0.8rem;
        margin-bottom: 0.5rem;
        border-radius: 4px;
        font-size: 0.9rem;
    }

    .footer {
        background: linear-gradient(90deg, #0a0705 0%, #771F02 100%);
        color: #C5C3B9;
        text-align: center;
        padding: 2rem;
        margin-top: 4rem;
        border-radius: 10px;
    }

    .divider {
        height: 2px;
        background: linear-gradient(90deg, transparent, #771F02, transparent);
        margin: 2rem 0 3rem 0;
    }

    .contact-box {
        background: #0a0705;
        border-radius: 10px;
        padding: 2rem;
        box-shadow: 0 4px 15px #C5C3B9;
        border-left: 5px solid #771F02;
        margin-top: 2rem;
    }

    .contact-box h3 {
        color: #C5C3B9;
        margin-bottom: 1rem;
    }

    .contact-item {
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 1rem;
    }

    .contact-item strong {
        color: #C5C3B9;
        min-width: 100px;
    }

    html,
    body,
    .stApp,
    .main,
    [data-testid="stAppViewContainer"],
    [data-testid="stHeader"],
    [data-testid="stMain"],
    [data-testid="stVerticalBlock"] {
        background: #0a0705 !important;
        background-color: #0a0705 !important;
        color: #C5C3B9;
    }

    .navbar,
    .hero-section,
    .footer {
        background: linear-gradient(90deg, #0a0705 0%, #771F02 100%) !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    }

    .section-title {
        color: #C5C3B9;
        border-bottom-color: #771F02;
    }

    .project-card,
    .skill-category,
    .contact-box {
        background: #0a0705 !important;
        color: #C5C3B9;
        box-shadow: 0 4px 15px rgba(96, 62, 38, 0.14);
        border-color: #771F02;
    }

    .project-card h3,
    .skill-category h4,
    .contact-box h3,
    .contact-item strong,
    .contact-item a {
        color: #C5C3B9;
    }

    .project-card p {
        color: #C5C3B9;
    }

    .tag {
        background-color: #0a0705;
        color: #C5C3B9;
        border: 1px solid #771F02;
    }

    .skill-item {
        background-color: #771F02;
        color: #C5C3B9;
    }

    .divider {
        background: linear-gradient(90deg, transparent, #771F02, transparent);
    }

    /* Icon grid for languages & tools */
    .icon-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1.2rem;
        margin: 1.5rem 0 2.5rem 0;
    }

    .icon-box {
        background-color: #0a0705;
        border: 2px solid #771F02;
        border-radius: 8px;
        aspect-ratio: 1 / 1;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 1.1rem;
        box-shadow: 0 4px 15px rgba(66, 56, 43, 0.25);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    .icon-box:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 20px rgba(119, 31, 2, 0.35);
    }

    .icon-box img {
        width: 65%;
        height: 65%;
        object-fit: contain;
    }

    .profile-photo-wrap {
        display: flex;
        justify-content: center;
        margin-bottom: 1rem;
    }

    .profile-photo {
        width: 220px;
        height: 220px;
        border-radius: 50%;
        overflow: hidden;
        border: 4px solid #771F02;
        box-shadow: 0 10px 24px rgba(119, 31, 2, 0.35);
        background: #0a0705;
    }

    .profile-photo img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        display: block;
    }

    .profile-photo.placeholder {
        display: flex;
        align-items: center;
        justify-content: center;
        color: #C5C3B9;
        font-weight: 700;
        text-align: center;
        padding: 1rem;
    }

    @media (max-width: 640px) {
        .icon-grid {
            grid-template-columns: repeat(2, 1fr);
        }
    }

    [data-testid="stMarkdownContainer"],
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] li,
    [data-testid="stMarkdownContainer"] span:not([style*="color"]),
    [data-testid="stMarkdownContainer"] strong,
    [data-testid="stMarkdownContainer"] a,
    [data-testid="stMarkdownContainer"] summary,
    [data-testid="stMarkdownContainer"] h1,
    [data-testid="stMarkdownContainer"] h2,
    [data-testid="stMarkdownContainer"] h3,
    [data-testid="stMarkdownContainer"] h4 {
        color: #C5C3B9 !important;
        text-shadow: 0 0 4px rgba(119, 31, 2, 0.45), 0 0 1px rgba(119, 31, 2, 0.6);
    }

    [data-testid="stMarkdownContainer"] h2,
    [data-testid="stMarkdownContainer"] h3,
    [data-testid="stMarkdownContainer"] summary {
        text-shadow: 0 0 8px rgba(119, 31, 2, 0.7), 0 0 2px rgba(119, 31, 2, 0.9);
    }

       with a subtle matching glow */
    [data-testid="stMarkdownContainer"] span.accent-highlight {
        color: #771F02 !important;
        text-shadow: 0 0 6px rgba(119, 31, 2, 0.5);
    }

    [data-testid="stAlert"] {
        background-color: transparent !important;
        background: transparent !important;
        border: 1px solid rgba(119, 31, 2, 0.75);
        border-radius: 8px;
        box-shadow: 0 0 18px rgba(119, 31, 2, 0.35), 0 0 40px rgba(119, 31, 2, 0.15), inset 0 0 20px rgba(119, 31, 2, 0.06);
        transition: box-shadow 0.3s ease;
    }

    [data-testid="stAlert"]:hover {
        box-shadow: 0 0 22px rgba(119, 31, 2, 0.5), 0 0 55px rgba(119, 31, 2, 0.22), inset 0 0 24px rgba(119, 31, 2, 0.1);
    }

    [data-testid="stAlert"] > div {
        background: transparent !important;
    }

    [data-testid="stAlert"] p,
    [data-testid="stAlert"] span,
    [data-testid="stAlert"] div {
        color: #C5C3B9 !important;
        text-shadow: 0 0 6px rgba(119, 31, 2, 0.55), 0 0 2px rgba(119, 31, 2, 0.7);
    }
</style>
""", unsafe_allow_html=True)


def render_profile_photo(image_path: str = "assets/profile.jpg", size: int = 220) -> None:
    path = Path(image_path)
    if path.exists():
        image_type = "jpeg" if path.suffix.lower() in {".jpg", ".jpeg"} else path.suffix.lower().lstrip(".") or "png"
        image_b64 = base64.b64encode(path.read_bytes()).decode("utf-8")
        st.markdown(
            f"""
            <div class="profile-photo-wrap">
                <div class="profile-photo" style="width:{size}px; height:{size}px;">
                    <img src="data:image/{image_type};base64,{image_b64}" alt="Profile photo" />
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""
            <div class="profile-photo-wrap">
                <div class="profile-photo placeholder" style="width:{size}px; height:{size}px;">
                    Add<br>assets/profile.jpg
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_icon_box(image_path: str, alt_text: str) -> str:
    path = Path(image_path)
    if not path.exists():
        return f'<div class="icon-box"><span style="font-size:0.8rem; text-align:center;">{alt_text}</span></div>'

    mime_type = "image/svg+xml" if path.suffix.lower() == ".svg" else f"image/{path.suffix.lower().lstrip('.') or 'png'}"
    image_b64 = base64.b64encode(path.read_bytes()).decode("utf-8")
    return f'<div class="icon-box"><img src="data:{mime_type};base64,{image_b64}" alt="{alt_text}"></div>'

def render_icon_grid(items: list[tuple[str, str]]) -> None:
    html = '<div class="icon-grid">' + "".join(render_icon_box(path, label) for path, label in items) + "</div>"
    st.markdown(html, unsafe_allow_html=True)


def render_social_icons() -> None:
    social_items = [
        ("assets/github-logo.svg", "https://github.com/Dmeymen"),
        ("assets/linkedin-logo.svg", "https://www.linkedin.com/in/dunameyamendoza"),
        ("assets/x-logo.svg", "https://x.com/Cynmeya_27"),
        ("assets/gmail-logo.svg", "mailto:dmeyamendoza@gmail.com"),
    ]

    html = '<div class="social-links">'
    for icon_path, link in social_items:
        path = Path(icon_path)
        if path.exists():
            image_b64 = base64.b64encode(path.read_bytes()).decode("utf-8")
            html += f'<a href="{link}" class="social-icon-btn" target="_blank"><img src="data:image/svg+xml;base64,{image_b64}" alt="Social icon"/></a>'
        else:
            html += f'<a href="{link}" class="social-icon-btn" target="_blank">•</a>'
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)


# Social Media Links at the top of the page
render_social_icons()

about_tab, projects_tab = st.tabs(["About / Skills", "Projects"])

with about_tab:
    # About section
    st.markdown('<h2 class="section-title">Hi, I\'m <span class="accent-highlight" style="font-weight:700; color: #771F02;">Duna</span></h2>', unsafe_allow_html=True)
    col1, col2 = st.columns([1.5, 1])

    with col1:
        st.markdown(
            textwrap.dedent(
                """
                <div style="padding-top: 2.5rem;">
                <p>
                    <span class="accent-highlight" style="font-weight:700; color: #771F02;">Curious</span> by nature.
                    <span class="accent-highlight" style="font-weight:700; color: #771F02;">Trained</span> in science.
                    <span class="accent-highlight" style="font-weight:700; color: #771F02;">Inspired</span> by art.
                </p>
                <p>
                Hi Everyone! I'm Duna Meya from Barcelona.<br>
                I'm a junior engineer pursuing a bachelor's degree in AI & Data Science engineering at LaSalle Campus University Ramon Llull.<br>
                I'm curious about technological innovation, and I enjoy exploring the intersection of science, art, and technology.<br>
                My passion lies in creating solutions that are not only functional but also new and efficient.
                </p>
                <div style="margin-top: 1rem;">
                </div>

                """
            ),
            unsafe_allow_html=True
        )

    pdf_path = Path("assets/CV_Duna.pdf")
    if pdf_path.exists():
        st.download_button(
            label="Download my CV",
            data=pdf_path.read_bytes(),
            file_name="CV_Duna.pdf",
            mime="application/pdf",
        )
    else:
        st.write("CV not found: assets/CV_Duna.pdf")

    with col2:
        render_profile_photo()
        st.info(
            "Additional information:\n\n"
            "🍪 **Location**: Barcelona, Spain\n\n"
            "🍰 **Education**: Bachelor's degree in AI & Data Science engineering at LaSalle Campus University Ramon Llull\n\n"
            "🧋 **Interest**: Sketching, Travelling, Graphic Design, Space"
        )

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # Skills Section
    st.markdown('<h2 class="section-title">Professional <span class="accent-highlight" style="font-weight:700; color: #771F02;">Skills</span></h2>', unsafe_allow_html=True)
    render_icon_grid([
        ("assets/c.svg", "C"),
        ("assets/java.svg", "Java"),
        ("assets/mysql-icon.svg", "MySQL"),
        ("assets/python.svg", "Python"),
    ])

    st.markdown('<h2 class="section-title"><span class="accent-highlight" style="font-weight:700; color: #771F02;">Tools</span> I Use</h2>', unsafe_allow_html=True)
    render_icon_grid([
        ("assets/intellij-idea.svg", "IntelliJ IDEA"),
        ("assets/clion.svg", "CLion"),
        ("assets/datagrip.svg", "DataGrip"),
        ("assets/webstorm.svg", "WebStorm"),
        ("assets/pycharm.svg", "PyCharm"),
        ("assets/visual-studio-code.svg", "VS Code"),
    ])

with projects_tab:
    # Project Section
    st.markdown('<h2 class="section-title">Featured Projects</h2>', unsafe_allow_html=True)

    projects = [
        {
            "title": "Creation of OS system - The Cytadel",
            "description": "A decentralized distributed application where independent nodes communicate, route data, and manage diplomacy and trade through concurrent processes without relying on a central server.",
            "details": '''
                <p><span class="accent-highlight" style='font-weight:700; color: #771F02;'>Core Technologies:</span> C, POSIX Threads (pthreads), Sockets (TCP/IP), Binary I/O, IPC (Inter-Process Communication), Makefile, MD5 Verification.</p>

                <p>The Citadel System is a decentralized, multi-process distributed application designed to establish a network of communication, diplomacy, and trade between independent nodes (representing "Great Houses" or Realms). Operating without a centralized server, each independent node acts as a router capable of handling multihops, dynamically routing files and control data across a network topology based on localized configuration files.</p>

                <p>The primary architecture centers on a Maester (the main node process) and a pool of concurrent, decoupled Envoy assistant processes delegated to manage active network I/O operations without stalling system control.</p>

                <p><span class="accent-highlight" style='font-weight:700; color: #771F02;'>Key Implementation Phases:</span></p>
                <ul class="fancy-list">
                    <li>Node Control &amp; Interface: Engineered the Maester main process, incorporating custom binary file parsers for inventory management (stock.db) and a modular, non-blocking case-insensitive command terminal utilizing standard system I/O (read/write system calls only).</li>
                    <li>Dynamic Multi-hop Routing &amp; Networking: Implemented standard network sockets to construct the peer-to-peer network matrix. Built an algorithmic routing subsystem that validates frame checksums and routes communications across neighbor nodes via configured or default paths.</li>
                    <li>Robust Data &amp; File Transfer Protocol: Built a fragmented custom protocol to handle binary file transmission (for political alliance sigils and trade ledger transactions). Incorporated runtime integrity checking using md5sum process integration and precise byte padding.</li>
                    <li>Internal Process Concurrency: Scaled the system to delegate dynamic networking pipelines concurrently. Implemented process forking (fork) and robust synchronization metrics to coordinate live communication pipelines between the main node and its array of Envoy subprocesses.</li>
                </ul>

                <p><span class="accent-highlight" style='font-weight:700; color: #771F02;'>Core Technical Highlights &amp; Engineering Challenges:</span></p>
                <ul class="fancy-list">
                    <li>Strict Low-Level Constraints: Developed entirely under strict system requirements prohibiting high-level library functions (such as printf, scanf, or standard wrapper libraries). All user terminal logs and file transfers were executed strictly via low-level read() and write() system calls to emphasize structural core system comprehension.</li>
                    <li>Concurrency &amp; Coordination: Designed complex, multi-threaded inter-process synchronization structures to decouple asynchronous network wait-times from the responsive user shell interface.</li>
                    <li>Fault Tolerance &amp; Reliability: Handled graceful structural exits, memory deallocation, and interrupt signals (CTRL+C). Managed communication edge cases including timeout drops, corrupt frame checksum validation, and node disconnect crash mitigations.</li>
                </ul>
            ''',
            "tags": ["C", "POSIX Threads", "IPC"],
            "link": "https://github.com/Dmeymen/TheCytadel"
        },
        {
            "title": "Object-Oriented Programming - Nude Eye Project",
            "description": "A console-based marketplace to purchase items, designed for object-oriented programming principles, data persistence, and layered architecture, with future extensibility in mind.",
            "details": '''
                <p><span class="accent-highlight" style='font-weight:700; color: #771F02;'>Core Technologies:</span> Java, JSON, CSV, UML diagrams, Class diagrams, JavaDoc, File I/O, GRASP principles, layered architecture.</p>

                <p>The Nude Eye Project is a console-based marketplace for buying and selling eyewear, developed in Java as a Minimum Viable Product (MVP) for Phases 1 and 2. It allows users to register, log in, search products by name or supplier, view their profile with purchase history, and manage a shopping cart with checkout. Data persistence is handled via JSON files (products, suppliers, clients) and CSV files (sales history), with all information read from and written to disk on demand.</p>

                <p>Designed with object-oriented principles, the system follows a layered architecture (presentation, business logic, persistence) and applies key GRASP patterns, such as Information Expert, Controller, and Polymorphism, to ensure low coupling and high cohesion. This design also anticipates future extensions, like varying VAT calculations and new customer types, as outlined for Phases 3 and 4. The project is documented with UML class diagrams and JavaDoc, following a phased delivery schedule.</p>

                <p><span class="accent-highlight" style='font-weight:700; color: #771F02;'>Key Implementation Phases:</span></p>
                <ul class="fancy-list">
                    <li>(Design) Create a UML class diagram defining the core domain classes (Product, Supplier, Client, Sale, Cart) and their relationships, applying encapsulation and abstraction.</li>
                    <li>(Implementation) Write the Java code based on the Phase 1 diagram. Implement console menus, JSON/CSV file I/O, and all MVP functionalities (registration, login, product search, profile, cart, checkout). Include JavaDoc documentation.</li>
                    <li>(Design) Extend the class diagram to support new requirements: different product types, customer tiers (B2B, online), and flexible pricing/VAT rules. Apply inheritance and polymorphism to handle variations cleanly.</li>
                    <li>(Implementation) Implement the extended design in Java, integrating the new features into the existing codebase.</li>
                </ul>

                <p><span class="accent-highlight" style='font-weight:700; color: #771F02;'>Core Technical Highlights &amp; Engineering Challenges:</span></p>
                <ul class="fancy-list">
                    <li>Object-oriented design: Full application of encapsulation, abstraction, inheritance, and polymorphism. Classes are designed with single responsibilities and clear boundaries between layers, following a layered architecture that separates Presentation (console menus), Business Logic (services), and Persistence (repositories) — ensuring low coupling and high cohesion.</li>
                    <li>Data persistence: Dual-format storage — JSON for structured entities (products, suppliers, clients) and CSV for flat sales history. All data is read/written on demand, with no unnecessary in-memory caching. File validation uses startup checks that ensure critical files (products.json, providers.json) exist and are well-formed, with graceful degradation when optional files (clients.json, sales.csv) are missing — they are created on first use.</li>
                    <li>Scalability for Phases 3 &amp; 4: New product types, customer roles, and pricing rules can be added without rewriting existing code, following the Open/Closed Principle — classes are open for extension (new subclasses) but closed for modification (existing code remains untouched), using interfaces and abstract classes liberally.</li>
                </ul>
            ''',
            "tags": ["Java", "JSON", "UML", "Layered Architecture"],
            "link": "https://github.com/Dmeymen/Nude_Eye_Project"
        },
        {
            "title": "Databases creation - Olympics Database",
            "description": "Design and implementation of a relational database for storing and managing Olympic Games data.",
            "details": '''
               <p><span class="accent-highlight" style='font-weight:700; color: #771F02;'>Core Technologies:</span> MySQL, Entity Model, Relational Model, Data cleaning, Database design, Query design.</p>

               <p>The Olympics Database is a relational database designed to store and manage data for the Olympic Games. It includes tables for athletes, events, countries, and results, with relationships defined to ensure data integrity and facilitate complex queries.</p>

               <p>The project is designed in three main stages, with each stage building upon the previous one to deliver a comprehensive solution with proper database design meant for scalability.</p>

               <p><span class="accent-highlight" style='font-weight:700; color: #771F02;'>Key Implementation Phases:</span></p>
               <ul class="fancy-list">
                   <li>Stage 1: Define relationships, applying encapsulation and abstraction, create the models of the data (both entity and relational models).</li>
                   <li>Stage 2: Write the SQL scripts to create the database schema and populate it with initial data.</li>
                   <li>Stage 3: Implement the application logic to interact with the database, including queries, verifications and triggers.</li>
               </ul>

               <p><span class="accent-highlight" style='font-weight:700; color: #771F02;'>Core Technical Highlights &amp; Engineering Challenges:</span></p>
               <ul class="fancy-list">
                    <li>Data cleaning for Oracle use: Managing data inconsistencies and ensuring data quality for Oracle database compatibility, this way allowing the platform to handle the data without setbacks; separating messy data from the main entities into their designated attributes for proper handling.</li>
                    <li>Proper insertion of data: Creating a script to properly insert the data, being mindful of table relationships and keys, as well as the creation of joint tables to support the relationships designated in the previous stage. Moreover, the generation of additional attributes such as IDs for easier tracking on later stages was also key for the overall correctness of the project.</li>
                    <li>Creation of queries and triggers: Developing efficient SQL queries and implementing database triggers to automate certain operations and maintain data integrity as requested. Additionally, each query adn trigger was paired with their verification so as to ensure their functionality.</li>
               </ul>
            ''',
            "tags": ["MySQL", "Data Cleaning", "Data Analysis"],
            "link": "#"
        },
        {
            "title": "Machine Learning - UraniaEr@vna - Galaxy Morphology Classification System",
            "description": "Development of a machine learning system for classifying galaxy morphologies.",
            "details": '''
               <p><span class="accent-highlight" style='font-weight:700; color: #771F02;'>Core Technologies:</span> Autoencoder, Convolutional Neural Networks (CNNs), K-Means Clustering, Gradient Boosting Classifier, FITS Files, StandardScaler, Streamlit, TensorFlow, scikit-learn, Astropy, Early Stopping, Multi-Input Neural Networks, Redshift Prediction.</p>

               <p>This project implements an automated galaxy classification pipeline that processes astronomical FITS images and metadata to predict both morphological type and redshift. The system employs an unsupervised convolutional autoencoder to compress 64x64 galaxy images into 128-dimensional visual fingerprints, which are then combined with CAS morphological parameters, Sérsic index, and bulge-to-total ratio to create a 133-dimensional feature vector.</p>

               <p>K-Means clustering generates pseudo-labels for six galaxy types (Elliptical, Spiral, Barred Spiral, Lenticular, Edge-On, Irregular), which a Gradient Boosting Classifier learns to reproduce with 0.95 accuracy. A separate multi-input CNN simultaneously predicts redshift values using both image data and Sérsic index. The complete pipeline is deployed as an interactive Streamlit web application allowing users to upload FITS files, visualize galaxies with adjustable colormaps and stretches, and download professional-formatted PDF reports.</p>

               <p><span class="accent-highlight" style='font-weight:700; color: #771F02;'>Key Implementation Phases:</span></p>
               <ul class="fancy-list">
                   <li>Data acquisition and preprocessing: Downloaded the COSMOS dataset with 100,000 FITS files and implemented a loader to read images, apply background subtraction and log scaling, resize to 64x64, and extract CAS parameters, Sérsic index, and BTT values from catalog metadata.</li>
                   <li>Model development and training: Built an autoencoder for 128-dimensional feature extraction, ran K-Means clustering on combined feature vectors, applied rule-based label mapping using BTT and Sérsic thresholds, trained a Gradient Boosting Classifier achieving 0.95 accuracy, and developed a multi-input CNN for redshift prediction.</li>
                   <li>Evaluation and analysis: Assessed classifier performance through confusion matrices and confidence histograms, evaluated redshift CNN with MAE of 1.459 and negative R² of -0.645, visualized feature space separation via PCA, and verified cluster averages matched known astronomical properties.</li>
                   <li>Application deployment and integration: Built a Streamlit web interface with four interactive tabs, implemented backend model loading and real-time visualization with adjustable colormaps, generated downloadable PDF reports with professional branding, and added error handling for robust user experience.</li>
               </ul>

               <p><span class="accent-highlight" style='font-weight:700; color: #771F02;'>Core Technical Highlights &amp; Engineering Challenges:</span></p>
               <ul class="fancy-list">
                    <li>Unsupervised classification without ground truth labels: The COSMOS dataset lacks morphological labels, requiring an innovative pipeline combining autoencoder feature extraction, K-Means clustering for pseudo-labels, and heuristic rule-based mapping using BTT and Sérsic index, achieving 0.95 classifier accuracy despite no manually labeled data, though this reflects agreement with K-Means rather than true astronomical truth.</li>
                    <li>Multi-modal feature integration for galaxy characterization: Heterogeneous data types including visual pixels, CAS parameters, Sérsic index, and BTT were combined into a 133-dimensional vector using StandardScaler to harmonize different numerical ranges, with PCA visualization confirming clear separation between morphological types in feature space.</li>
                    <li>Computational constraints and training optimization: Processing thousands of FITS files on Google Colab required binary serialization to save preprocessed data and avoid repeated I/O operations, while a simplified 1,000-sample backend enabled rapid debugging, yet the redshift CNN still performed poorly due to the difficulty of photometric redshift estimation from low-resolution single-band images.</li>
               </ul>
            ''',
            "tags": ["Python", "Machine Learning", "Clustering", "Tensorflow", "Autoencoders", "UI"],
            "link": "#"
        }
    ]

    def strip_lines(text):
        """Remove all leading whitespace from every line so Markdown never
        mistakes indented HTML for a code block."""
        return "\n".join(line.strip() for line in text.strip().splitlines())

    for project in projects:
        tags_html = "".join([f'<span class="tag">{tech}</span>' for tech in project["tags"]])
        details_html = strip_lines(project["details"])
        card_html = strip_lines(f"""
            <details class="project-card">
            <summary>{project['title']}</summary>
            <div class="project-details">
            <p>{project['description']}</p>
            {details_html}
            <div class="tags">{tags_html}</div>
            <a href="{project['link']}" class="social-btn" target="_blank">View on GitHub</a>
            </div>
            </details>
        """)
        st.markdown(card_html, unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)