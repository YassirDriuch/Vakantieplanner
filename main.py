import locale


from ui.menu import hoofdmenu

def main():
    # Locale wordt gebruikt voor nummer format (om populatiegrootte duidelijker weer te geven)
    locale.setlocale(locale.LC_ALL, "")



    # Start de applicatie
    hoofdmenu()


if __name__ == "__main__":
    main()