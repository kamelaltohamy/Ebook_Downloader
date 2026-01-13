# **Archive-Automator: Python E-Book Organizer 📚**

An automated web scraping tool built with **Python**, **Tkinter**, and **BeautifulSoup**. This tool is designed to crawl digital archives, extract book metadata (Title, Author, Cover Image), and organize them into a clean, hierarchical folder structure.

## **✨ Features**

* **Organized Downloads:** Automatically creates a separate folder for every book.  
* **Metadata Extraction:** Saves author info and source URLs into a local info.txt for every entry.  
* **GUI Interface:** Easy-to-use Tkinter window with range selection (start ID to end ID).  
* **Smart Progress Tracking:** Real-time log console and progress bar.  
* **Multi-threaded:** The UI stays responsive while the scraper works in the background.  
* **Resilient:** Includes error handling for missing pages or failed downloads.

## **📸 Screenshots**

**Tip for GitHub:** To display an image here, upload your screenshot to a folder named assets in your repository, then use the link below:

*Example of the GUI and the organized folder structure.*

## **🚀 Getting Started**

### **Prerequisites**

You will need Python 3.7 or higher installed on your machine.

### **Installation**

1. **Clone the repository:**  
   git clone \[https://github.com/yourusername/Archive-Automator.git\](https://github.com/yourusername/Archive-Automator.git)  
   cd Archive-Automator

2. **Install dependencies:**  
   pip install requests beautifulsoup4

3. **Run the application:**  
   python book\_scraper.py

## **🛠️ Built With**

* [Requests](https://requests.readthedocs.io/) \- Elegant and simple HTTP library.  
* [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/) \- For parsing HTML and extracting data.  
* [Tkinter](https://docs.python.org/3/library/tkinter.html) \- Python's de-facto standard GUI package.

## **📁 Project Structure**

Archive-Automator/  
│  
├── book\_scraper.py      \# Main application script  
├── README.md            \# Documentation  
├── .gitignore           \# Prevents uploading downloaded content  
└── Downloaded\_Books/    \# (Generated) Local storage for books  
    └── \[Book\_ID\]\_\[Name\]/  
        ├── \[Name\].pdf  
        ├── cover.jpg  
        └── info.txt

## **📜 Legal Disclaimer**

This tool is for **educational purposes and personal use only**. It is designed to demonstrate web scraping techniques and automation logic. When using this tool, please:

1. Respect the website's robots.txt file.  
2. Do not overload the server with rapid requests.  
3. Ensure you have the right to download the content for personal study.

## **📄 License**

This project is licensed under the MIT License \- see the [LICENSE](https://www.google.com/search?q=LICENSE) file for details.

## **💡 How to make your README look powerful**

1. **Add Badges:** I used [Shields.io](https://shields.io/) for the badges at the top.  
2. **Add Images:**  
   * Create a folder in your repo called assets.  
   * Upload your image (e.g., screenshot.png).  
   * Use this syntax: \!\[Alt Text\](assets/screenshot.png).  
3. **Use Emojis:** They make the documentation more readable and friendly.  
4. **Add a GIF:** Use a screen recorder (like Kap or OBS) to create a short GIF of the app working. It proves the code actually works\!