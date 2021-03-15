import argparse
import qrcode


major = "1"
minor = "1"
micro = "0"

__version__ = ".".join([major, minor, micro])


def get_input():
    data = ""
    # If the user doesn't enter anything and cause a EOF error, This will avoid a UnboundLocalError
    z = ""
    while True:
        try:
            z = input(
                "Enter content, To end it, press Ctrl-Z on windows, or Ctrl-D on linux: ")
            data += z
            z = ""
        except EOFError:
            return data + z


def _main(args=None):
    print("QR-Creator v{}, Easily create QR codes, Written by TheOddZer0".format(__version__))
    print("See COPYING for me info")
    print("See original repo for updates, more info: https://github.com/TheOddZer0/QR-Creator")
    print("")
    parser = argparse.ArgumentParser()
    parser.add_argument("--fore-color", "-fc",
                        help="Which color to use as the foreground color, defaults to 'black'",
                        default="black", action="store",
                        )
    parser.add_argument("--back-color", "-bc",
                        help="Which color to use as the background color, defaults to 'white'",
                        default="white", action="store",
                        )

    parser.add_argument("--border", "-b",
                        help="Increase or decrease the thickness of border, defaults to '4' and cannot be lower then",
                        default=4, type=int, action="store",
                        )

    parser.add_argument("--input", "-in",
                        help="Instead of reading from STDIN, Read the content of the file",
                        default=None, action="store",
                        )
    parser.add_argument("--size", "-s",
                        help="Increase the size, defaults to whatever suits your data, the biggest is 40",
                        default=None, action="store", type=int,
                        )
    parser.add_argument("--output", "-o",
                        help="Which file to store output as, defaults to 'Output'",
                        default="out", action="store",
                        )
    parser.add_argument("--kind", "-k",
                        help="What kind of picture do you want, defaults to 'png'",
                        default="png", action="store",
                        )

    ns = parser.parse_args(args)
    if ns.border < 4:
        print("'Boarder' cannot be lower then 4, going with 4")
        ns.border = 4
    elif ns.size is not None and 0 > ns.size > 40:
        print("'Size' cannot be lower then 1 or bigger then 40, going with the most suitable for your data")
        ns.size = None

    qr = qrcode.QRCode(version=ns.size, border=ns.border)
    if ns.input:
        try:
            with open(ns.input, "r") as f:
                data = f.read()
        except FileNotFoundError:
            print("Cannot open '{}', File doesn't exist".format(ns.input))
        except PermissionError:
            print("Cannot open '{}', Insufficient permissions".format(ns.input))
    else:
        data = get_input()
    try:
        qr.add_data(data)
        qr.make()
        factory = qr.make_image(fill_color=ns.fore_color,
                                back_color=ns.back_color)
        factory.kind = ns.kind
    except:
        print("Unhandled exception happened, Please report this on github to TheOddZer0")
        raise
    try:
        factory.save(ns.output + "." + ns.kind)
    except KeyError:
        print("Unknown format '{}', falling back on 'png'".format(ns.kind))
        factory.save(ns.output + ".png", format="png")
        print("Done, Operation was successful")
        
def main():
    try:
        _main()
    except KeyboardInterrupt:
        print("User requested exit, exiting...")

if __name__ == '__main__':
    main()