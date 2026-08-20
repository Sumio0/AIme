from pylatex import Document, Section, Subsection, Command, MiniPage, LineBreak, VerticalSpace
from pylatex.base_classes import Environment
from pylatex.package import Package
from pylatex.utils import NoEscape, bold, italic

class TemplateGenerator:
    """Class to manage different LaTeX resume templates"""
    
    @staticmethod
    def create_professional_template(resume_data):
        """Create a professional LaTeX resume template"""
        # Basic document setup with custom margins
        geometry_options = {
            "margin": "0.7in",
            "top": "0.6in",
            "bottom": "0.6in"
        }
        doc = Document(geometry_options=geometry_options)
        
        # Add packages
        doc.packages.append(Package('fontawesome'))
        doc.packages.append(Package('hyperref', options='hidelinks'))
        doc.packages.append(Package('xcolor'))
        doc.packages.append(Package('titlesec'))
        doc.preamble.append(NoEscape(r'\definecolor{primary}{RGB}{0, 102, 204}'))
        doc.preamble.append(NoEscape(r'\titleformat{\section}{\Large\bfseries\color{primary}}{\thesection}{0em}{}[\titlerule]'))
        
        # Header with name and contact info
        with doc.create(MiniPage(width=r'1\textwidth', align='c')):
            doc.append(NoEscape(r'\begin{center}'))
            doc.append(NoEscape(r'{\Huge\textbf{' + resume_data.get('name', 'Your Name') + r'}}\\[0.5em]'))
            doc.append(NoEscape(r'\begin{tabular}{c c c}'))
            
            if resume_data.get('email'):
                doc.append(NoEscape(r'\faEnvelope\ ' + resume_data.get('email') + r' & '))
            
            if resume_data.get('phone'):
                doc.append(NoEscape(r'\faPhone\ ' + resume_data.get('phone') + r' & '))
            
            if resume_data.get('location'):
                doc.append(NoEscape(r'\faMapMarker\ ' + resume_data.get('location')))
            
            doc.append(NoEscape(r'\end{tabular}'))
            doc.append(NoEscape(r'\end{center}'))
        
        # Education section
        doc.append(VerticalSpace("0.5cm"))
        with doc.create(Section('Education')):
            for edu in resume_data.get('education', []):
                doc.append(NoEscape(r'\textbf{' + edu.get('school', '') + r'}, ' + edu.get('location', '') + r'\hfill ' + edu.get('start_date', '') + r' - ' + edu.get('end_date', '') + r'\\'))
                doc.append(NoEscape(r'\textit{' + edu.get('degree', '') + r', ' + edu.get('major', '') + r'}\\'))
                doc.append(VerticalSpace("0.3cm"))
        
        # Experience section
        with doc.create(Section('Work Experience')):
            for exp in resume_data.get('experience', []):
                doc.append(NoEscape(r'\textbf{' + exp.get('company', '') + r'}, ' + exp.get('location', '') + r'\hfill ' + exp.get('start_date', '') + r' - ' + exp.get('end_date', '') + r'\\'))
                doc.append(NoEscape(r'\textit{' + exp.get('position', '') + r'}\\'))
                doc.append(exp.get('description', ''))
                doc.append(VerticalSpace("0.3cm"))
        
        # Skills section
        with doc.create(Section('Skills')):
            skills = resume_data.get('skills', [])
            if skills:
                doc.append(NoEscape(r'\begin{itemize}'))
                for skill in skills:
                    doc.append(NoEscape(r'\item ' + skill))
                doc.append(NoEscape(r'\end{itemize}'))
        
        return doc
    
    @staticmethod
    def create_academic_template(resume_data):
        """Create an academic LaTeX resume template, suitable for research or academic positions"""
        # Basic document setup with standard article class
        doc = Document('article')
        
        # Add packages
        doc.packages.append(Package('hyperref', options='hidelinks'))
        doc.packages.append(Package('geometry', options='margin=1in'))
        
        # Name and contact info
        doc.append(NoEscape(r'\begin{center}'))
        doc.append(NoEscape(r'{\Large\bfseries ' + resume_data.get('name', 'Your Name') + r'}\\'))
        doc.append(NoEscape(r'\vspace{0.1cm}'))
        
        contact_parts = []
        if resume_data.get('email'):
            contact_parts.append(resume_data.get('email'))
        if resume_data.get('phone'):
            contact_parts.append(resume_data.get('phone'))
        if resume_data.get('location'):
            contact_parts.append(resume_data.get('location'))
        
        doc.append(NoEscape(r' $\mid$ '.join(contact_parts)))
        doc.append(NoEscape(r'\end{center}'))
        
        # Education section with clean formatting
        doc.append(NoEscape(r'\section*{\centering Education}'))
        doc.append(NoEscape(r'\hrulefill'))
        
        for edu in resume_data.get('education', []):
            doc.append(NoEscape(r'\vspace{0.2cm}'))
            doc.append(NoEscape(r'\textbf{' + edu.get('degree', '') + r' in ' + edu.get('major', '') + r'}'))
            doc.append(NoEscape(r'\hfill ' + edu.get('start_date', '') + r' - ' + edu.get('end_date', '') + r'\\'))
            doc.append(NoEscape(edu.get('school', '') + r', ' + edu.get('location', '') + r'\\'))
        
        # Experience section
        doc.append(NoEscape(r'\section*{\centering Experience}'))
        doc.append(NoEscape(r'\hrulefill'))
        
        for exp in resume_data.get('experience', []):
            doc.append(NoEscape(r'\vspace{0.2cm}'))
            doc.append(NoEscape(r'\textbf{' + exp.get('position', '') + r'}'))
            doc.append(NoEscape(r'\hfill ' + exp.get('start_date', '') + r' - ' + exp.get('end_date', '') + r'\\'))
            doc.append(NoEscape(exp.get('company', '') + r', ' + exp.get('location', '') + r'\\'))
            doc.append(NoEscape(exp.get('description', '') + r'\\'))
        
        # Skills section
        doc.append(NoEscape(r'\section*{\centering Skills}'))
        doc.append(NoEscape(r'\hrulefill'))
        
        skills = resume_data.get('skills', [])
        if skills:
            doc.append(NoEscape(r'\begin{center}'))
            doc.append(NoEscape(', '.join(skills)))
            doc.append(NoEscape(r'\end{center}'))
        
        return doc
    
    @staticmethod
    def create_modern_template(resume_data):
        """Create a modern, stylish LaTeX resume template"""
        # Setting up a more modern document with custom styling
        geometry_options = {
            "left": "0.7in",
            "right": "0.7in",
            "top": "0.7in",
            "bottom": "0.7in"
        }
        doc = Document(geometry_options=geometry_options)
        
        # Add required packages
        doc.packages.append(Package('fontawesome'))
        doc.packages.append(Package('titlesec'))
        doc.packages.append(Package('enumitem'))
        doc.packages.append(Package('xcolor'))
        doc.packages.append(Package('hyperref', options='colorlinks,linkcolor=blue,urlcolor=blue'))
        
        # Custom styling
        doc.preamble.append(NoEscape(r'\definecolor{highlight}{RGB}{41, 128, 185}'))
        doc.preamble.append(NoEscape(r'\titleformat{\section}{\Large\scshape\raggedright\color{highlight}}{}{0em}{}[\titlerule]'))
        doc.preamble.append(NoEscape(r'\setlist[itemize]{leftmargin=*}'))
        
        # Header
        doc.append(NoEscape(r'{\Huge\bfseries\color{highlight} ' + resume_data.get('name', 'Your Name') + r'}\\'))
        doc.append(NoEscape(r'\vspace{0.3cm}'))
        
        # Contact row
        with doc.create(MiniPage(width=r'1\textwidth')):
            contact_parts = []
            
            if resume_data.get('email'):
                contact_parts.append(r'\faEnvelope\ ' + resume_data.get('email'))
            
            if resume_data.get('phone'):
                contact_parts.append(r'\faPhone\ ' + resume_data.get('phone'))
            
            if resume_data.get('location'):
                contact_parts.append(r'\faMapMarker\ ' + resume_data.get('location'))
            
            doc.append(NoEscape(' $\mid$ '.join(contact_parts)))
        
        # Education
        doc.append(NoEscape(r'\vspace{0.4cm}'))
        with doc.create(Section('Education')):
            for edu in resume_data.get('education', []):
                doc.append(NoEscape(r'\textbf{\large ' + edu.get('school', '') + r'}'))
                doc.append(NoEscape(r'\hfill\textit{' + edu.get('start_date', '') + r' - ' + edu.get('end_date', '') + r'}\\'))
                doc.append(NoEscape(r'\textit{' + edu.get('degree', '') + r' in ' + edu.get('major', '') + r'}'))
                doc.append(NoEscape(r', ' + edu.get('location', '') + r'\\'))
                doc.append(NoEscape(r'\vspace{0.2cm}'))
        
        # Experience
        with doc.create(Section('Professional Experience')):
            for exp in resume_data.get('experience', []):
                doc.append(NoEscape(r'\textbf{\large ' + exp.get('company', '') + r'}'))
                doc.append(NoEscape(r'\hfill\textit{' + exp.get('start_date', '') + r' - ' + exp.get('end_date', '') + r'}\\'))
                doc.append(NoEscape(r'\textcolor{highlight}{\textbf{' + exp.get('position', '') + r'}}'))
                doc.append(NoEscape(r', ' + exp.get('location', '') + r'\\'))
                
                # If description contains multiple sentences, format as bullet points
                description = exp.get('description', '')
                if '.' in description and len(description) > 100:
                    sentences = [s.strip() for s in description.split('.') if s.strip()]
                    doc.append(NoEscape(r'\begin{itemize}[leftmargin=*, topsep=0pt, partopsep=0pt]'))
                    for sentence in sentences:
                        doc.append(NoEscape(r'\item ' + sentence + '.'))
                    doc.append(NoEscape(r'\end{itemize}'))
                else:
                    doc.append(NoEscape(description + r'\\'))
                
                doc.append(NoEscape(r'\vspace{0.2cm}'))
        
        # Skills
        with doc.create(Section('Skills')):
            skills = resume_data.get('skills', [])
            if skills:
                doc.append(NoEscape(r'\begin{itemize}[leftmargin=*, topsep=0pt, partopsep=0pt]'))
                for i in range(0, len(skills), 3):  # Group skills into groups of 3
                    group = skills[i:i+3]
                    doc.append(NoEscape(r'\item ' + ' $\mid$ '.join(group)))
                doc.append(NoEscape(r'\end{itemize}'))
        
        return doc
    
    @staticmethod
    def create_creative_template(resume_data):
        """Create a creative, design-oriented resume template"""
        # Setting up a creative document with unique styling
        geometry_options = {
            "margin": "0.6in",
        }
        doc = Document(geometry_options=geometry_options)
        
        # Add creative styling required packages
        doc.packages.append(Package('fontawesome'))
        doc.packages.append(Package('tikz'))
        doc.packages.append(Package('xcolor'))
        doc.packages.append(Package('hyperref', options='colorlinks,linkcolor=orange,urlcolor=orange'))
        doc.packages.append(Package('titlesec'))
        doc.packages.append(Package('enumitem'))
        
        # Creative styling
        doc.preamble.append(NoEscape(r'\definecolor{accent}{RGB}{255, 165, 0}'))  # Orange accent color
        doc.preamble.append(NoEscape(r'\titleformat{\section}{\Large\bfseries}{}{0em}{\colorbox{accent!20}{\parbox{\dimexpr\textwidth-2\fboxsep\relax}{\thesection\ #1}}}'))
        doc.preamble.append(NoEscape(r'\titleformat{name=\section, numberless}{\Large\bfseries}{}{0em}{\colorbox{accent!20}{\parbox{\dimexpr\textwidth-2\fboxsep\relax}{#1}}}'))
        
        # Fancy header with name and design elements
        doc.append(NoEscape(r'\begin{center}'))
        doc.append(NoEscape(r'\begin{tikzpicture}'))
        doc.append(NoEscape(r'\node[rectangle, fill=accent!10, minimum width=\textwidth, minimum height=3cm, align=center] (box) {};'))
        doc.append(NoEscape(r'\node[text=black, align=center] at (box) {{\Huge\textbf{' + resume_data.get('name', 'Your Name') + r'}}\\[0.3cm]'))
        
        contact_parts = []
        if resume_data.get('email'):
            contact_parts.append(r'\faEnvelope\ ' + resume_data.get('email'))
        if resume_data.get('phone'):
            contact_parts.append(r'\faPhone\ ' + resume_data.get('phone'))
        if resume_data.get('location'):
            contact_parts.append(r'\faMapMarker\ ' + resume_data.get('location'))
        
        doc.append(NoEscape(' $\mid$ '.join(contact_parts) + r'};'))
        doc.append(NoEscape(r'\end{tikzpicture}'))
        doc.append(NoEscape(r'\end{center}'))
        
        # Education section with creative formatting
        doc.append(NoEscape(r'\vspace{0.5cm}'))
        with doc.create(Section('Education')):
            for edu in resume_data.get('education', []):
                doc.append(NoEscape(r'\begin{minipage}{\textwidth}'))
                doc.append(NoEscape(r'\textbf{\large ' + edu.get('school', '') + r'}'))
                doc.append(NoEscape(r'\hfill\textcolor{accent}{\textbf{' + edu.get('start_date', '') + r' - ' + edu.get('end_date', '') + r'}}\\'))
                doc.append(NoEscape(r'\textit{' + edu.get('degree', '') + r' in ' + edu.get('major', '') + r'}'))
                doc.append(NoEscape(r', ' + edu.get('location', '') + r'\\'))
                doc.append(NoEscape(r'\end{minipage}'))
                doc.append(NoEscape(r'\vspace{0.3cm}'))
        
        # Experience section with creative elements
        with doc.create(Section('Experience')):
            for exp in resume_data.get('experience', []):
                doc.append(NoEscape(r'\begin{minipage}{\textwidth}'))
                doc.append(NoEscape(r'\textbf{\large ' + exp.get('company', '') + r'}'))
                doc.append(NoEscape(r'\hfill\textcolor{accent}{\textbf{' + exp.get('start_date', '') + r' - ' + exp.get('end_date', '') + r'}}\\'))
                doc.append(NoEscape(r'\textcolor{accent}{\textbf{' + exp.get('position', '') + r'}}'))
                doc.append(NoEscape(r', ' + exp.get('location', '') + r'\\'))
                doc.append(NoEscape(r'\begin{tcolorbox}[colback=white!98!black, colframe=accent!20, boxrule=0.5pt]'))
                doc.append(NoEscape(exp.get('description', '')))
                doc.append(NoEscape(r'\end{tcolorbox}'))
                doc.append(NoEscape(r'\end{minipage}'))
                doc.append(NoEscape(r'\vspace{0.3cm}'))
        
        # Skills section with visual styling
        with doc.create(Section('Skills')):
            skills = resume_data.get('skills', [])
            if skills:
                doc.append(NoEscape(r'\begin{center}'))
                for skill in skills:
                    doc.append(NoEscape(r'\fcolorbox{accent!20}{accent!10}{\parbox{0.25\textwidth}{\centering ' + skill + r'}}'))
                    doc.append(NoEscape(r'\quad'))  # Add space between skill boxes
                doc.append(NoEscape(r'\end{center}'))
        
        return doc
    
    @staticmethod
    def get_template(template_style, resume_data):
        """Get the appropriate template based on style"""
        if template_style == 'professional':
            return TemplateGenerator.create_professional_template(resume_data)
        elif template_style == 'academic' or template_style == 'latex':
            return TemplateGenerator.create_academic_template(resume_data)
        elif template_style == 'creative':
            return TemplateGenerator.create_creative_template(resume_data)
        else:  # default to modern
            return TemplateGenerator.create_modern_template(resume_data) 