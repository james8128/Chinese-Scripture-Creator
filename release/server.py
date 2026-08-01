"""Serve the scripture reader from this folder (release/).

Plain HTTP only (no TLS). Open:
    http://127.0.0.1:8081/
NOT https://  — browsers that force HTTPS will get HTTP 400 errors.
"""
import http.server
import os
import socketserver
import sys
import webbrowser

PORT = 8081

# Document root = folder containing this script (…/release)
ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT)


class Handler(http.server.SimpleHTTPRequestHandler):
    extensions_map = {
        **getattr(http.server.SimpleHTTPRequestHandler, "extensions_map", {}),
        ".html": "text/html; charset=utf-8",
        ".js": "application/javascript; charset=utf-8",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
    }

    def log_message(self, format, *args):
        # Detect TLS ClientHello (\x16\x03…) sent to a plain HTTP port
        try:
            msg = args[0] if args else ""
            if isinstance(msg, str) and (
                msg.startswith(r"\x16") or msg.startswith("\x16") or "\\x16\\x03" in msg
            ):
                sys.stderr.write(
                    "\n*** Browser used HTTPS on this HTTP-only port. ***\n"
                    "*** Use:  http://127.0.0.1:%s/   (not https://) ***\n\n"
                    % PORT
                )
                return
        except Exception:
            pass
        super().log_message(format, *args)

    def handle_one_request(self):
        try:
            super().handle_one_request()
        except Exception:
            # Malformed / TLS garbage — ignore so the server keeps running
            pass


def main():
    socketserver.TCPServer.allow_reuse_address = True
    try:
        httpd = socketserver.TCPServer(("", PORT), Handler)
    except OSError as e:
        print(f"Could not bind to port {PORT}: {e}")
        print("Is another server already running on that port?")
        sys.exit(1)

    url = f"http://127.0.0.1:{PORT}/"
    print(f"Document root: {ROOT}")
    print()
    print(f"  Open this URL (HTTP, not HTTPS):")
    print(f"    {url}")
    print(f"    http://localhost:{PORT}/")
    print()
    print("  Do NOT use https:// — that causes: code 400 Bad request version")
    print("  If the browser upgrades to HTTPS, type the full http:// URL,")
    print("  or try http://127.0.0.1:8081/ instead of localhost.")
    print()
    print("Press Ctrl+C to stop.")

    # Open the correct http:// URL once (Windows / desktop convenience)
    try:
        webbrowser.open(url)
    except Exception:
        pass

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
    finally:
        httpd.server_close()


if __name__ == "__main__":
    main()
