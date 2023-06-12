import threading
import werkzeug.serving


from server import app
#from server.submit import submit_loop


if not werkzeug.serving.is_running_from_reloader():
    #threading.Thread(target=submit_loop.run_loop, daemon=True).start()
    pass
    # FIXME: Don't use daemon=True, exit from the thread properly