### videostreaming
### v0.2.6
### MikiTwenty

import socket, pickle, struct, cv2, sys, time

class Socket(object):
    def __init__(self, socket_type, show_ip, capture_video, video_source, verbose) -> None:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host_name = socket.gethostname()
        self.host_ip = socket.gethostbyname(self.host_name)
        self.socket_type = socket_type
        self.capture_video = capture_video
        self.video_source = video_source
        self.max_upload_speed = 10*1000*1024
        self.max_download_speed = 10*1000*1024
        self._set_verbosity(verbose)
        self.timed_out = False
        if show_ip:
            self._log(f"IP address: {self.host_ip}", self.verbosity_level[0])
        if self.capture_video:
            self._get_video()

    def _get_video(self):
        try:
            self._log("Initializing OpenCV video capture...", self.verbosity_level[2])
            self.video = cv2.VideoCapture(self.video_source)
            if self.video is None or not self.video.isOpened():
                self._log(f"Unable to open video source: {self.video_source}")
                exit()
        except Exception as error:
            raise(error)

    def _set_port(self):
        while True:
            port = input(f"{self.socket_type} Select port >> ")
            if len(port) == 4:
                try:
                    port = int(port)
                    break
                except:
                    self._log("Port must be an int!")
            else:
                self._log("Port must have 4 numbers!")
        return port

    def _get_size(self, send=False):
        """
        Get the camera frame size (MB).\n
        Parameters
        ----------
        - ``send`` (bool) : send the frame size to the connected socket (default: False).\n
        """
        try:
            capturing, frame = self.video.read(self.video_source)
            if capturing:
                frame_size = sys.getsizeof(frame) + 100
                self.max_upload_speed = frame_size
                self._log(f"Camera frame size: {(frame_size/(1000*1024)):.2f} MB", self.verbosity_level[2])
                if send:
                    try:
                        frame_size_binary = (bin(frame_size)).encode()
                        self.client_socket.sendall(frame_size_binary)
                        self._log(f"Frame size sent to: {self.client_socket.getsockname()[0]}", self.verbosity_level[2])
                    except Exception as error:
                        self._log(error)
        except Exception as error:
            raise(error)

    def _set_size(self, size=None):
        if not size:
            try:
                self.client_socket.settimeout(1)
                self.max_download_speed = int(self.client_socket.recv(10*1000*1024), 2)
                self.client_socket.setblocking(True)
                self._log(f"Get frame size from: {self.client_socket.getsockname()[0]}", self.verbosity_level[2])
            except Exception as error:
                self._log(error)
        else:
            try:
                size *= 1000*1024
                self.max_download_speed = size
                self._log("Upload speed set as default (10 MB)", self.verbosity_level[2])
            except Exception as error:
                raise(error)

    def send(self, frame:object=None, resolution:tuple=(640, 480), show_video:bool=False) -> None:
        """
        Send a frame to the connected socket.\n
        Parameters
        ----------
        - ``frame`` (object) : the frame to send.
        - ``resolution`` (tuple) : the frame resolution,
         must be a tuple (int, int), (default: (640, 480)).
        - ``show_video`` (bool) : show the outgoing video,
         it works with capture_video=True (default=False).
        """
        if self.capture_video:
            capturing, frame = self.video.read()
        else:
            capturing = True
        if capturing:
            try:
                frame = cv2.resize(frame, dsize=resolution)
            except Exception as error:
                raise(error)
            serialized_frame = pickle.dumps(frame)
            message = struct.pack("Q", len(serialized_frame)) + serialized_frame
            try:
                if show_video and self.capture_video:
                    cv2.imshow(f"{self.socket_type} Trasmitting video...", frame)
                    if cv2.waitKey(30) == 27:
                        cv2.destroyAllWindows()
                self.client_socket.sendall(message)
            except Exception as error:
                raise(error)

    def receive(self, show_video:bool=False) -> None:
        """
        Receive a frame from the connected socket.\n
        Parameters
        ----------
        - ``show_video`` (bool) : show the outgoing video,
         it works with capture_video=True (default=False).\n
        Returns
        -------
        - ``True`` | ``frame`` (object) : while receiving data.
        """
        data = b""
        payload_size = struct.calcsize("Q")
        try:
            while len(data) < payload_size:
                packet = self.client_socket.recv(self.max_download_speed)
                if not packet:
                    break
                data += packet
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("Q", packed_msg_size)[0]
            while len(data) < msg_size:
                data += self.client_socket.recv(self.max_download_speed)
                if not data:
                    break
            frame_data = data[:msg_size]
            data = data[msg_size:]
            frame = pickle.loads(frame_data)
            if show_video and self.capture_video:
                cv2.imshow(f"{self.socket_type} Receiving video...", frame)
                if cv2.waitKey(30) == 27:
                    cv2.destroyAllWindows()
            else:
                return True, frame
        except Exception as error:
            raise(error)

    def connected(self) -> socket.socket:
        """
        Check if a client is connected with the server.\n
        Returns
        -------
        - ``False`` (bool) : if no socket is connected.
        - ``socket`` (object) : if a socket is connected.
        """
        try:
            return self.client_socket
        except:
            return False

    def close(self) -> None:
        """
        Interrupt the connection with the connected socket.
        """
        self.socket.close()
        try:
            cv2.destroyAllWindows()
        except:
            pass
        self._log("Stopped")

    def _set_verbosity(self, verbose):
        if verbose == 'high' or verbose == 3:
            self.verbosity_level = [True, True, True]
            self._log("Verbosity set to: 'high'", self.verbosity_level[0])
        elif verbose == 'medium' or verbose == 2:
            self.verbosity_level = [True, True, False]
        elif verbose == 'low'or verbose == 1 or verbose == True:
            self.verbosity_level = [True, False, False]
        elif verbose == False or verbose == 0:
            self.verbosity_level = [False, False, False]
        else:
            self._log("Invalid verbosity value, see documentation.")

    def _log(self, string, verbose=True):
        try:
            if verbose:
                print(f"{self.socket_type} {string}")
        except Exception as error:
            raise(error)

class Server(Socket):
    def __init__(self, show_ip:bool=True, capture_video:bool=False, video_source:int=0, verbose:bool=True) -> None:
        """
        Streaming server socket.\n
        Parameters
        ----------
        - ``show_ip`` (bool) : self._log server IP address (default=True).
        - ``capture_video`` (bool) : enable video capturing with cameras (default=False).
        - ``video_source`` (int) : set camera index (default=0).
        - ``verbose`` (int | bool | str) : set verbosity level,
         it can be 'high' (or 3), 'medium' (or 2), 'low' (or True or 1),
         False (or 0) (default=True).\n
        Methods
        -------
        - ``connect()`` : open connections for a client socket.
        - ``send()`` : send a frame to the client socket.
        - ``receive()`` : receive a frame from the client socket.
        - ``connected()`` : check if the server is connected with a client.
        - ``disconnect()`` : interrupt all the connections and shut down the server.\n
        Example
        -------
        >>> server = Server()
        >>> server.connect()
        >>> while server.connected():
        >>>     server.receive()
        >>>     server.send()
        >>> server.disconnect()
        """
        super().__init__(socket_type="[Server]", show_ip=show_ip, capture_video=capture_video, video_source=video_source, verbose=verbose)
        self.server_socket = self.socket

    def connect(self, port:int=None, timeout:int=1, blocking:bool=False) -> None:
        """
        Wait for a client socket connection.\n
        Parameters
        ----------
        - ``port`` (int) : set the port to open for connections (default: False).
        - ``timeout`` (int) : set timeout to check for connections (default: 1).
        - ``blocking`` (bool) : looping when searching for connections (default: False).\n
        """
        try:
            self.server_socket.settimeout(timeout)
        except Exception as error:
            raise(error)
        if not self.timed_out:
            if not port:
                port = self._set_port()
            socket_address = (self.host_ip, port)
            try:
                self.server_socket.bind(socket_address)
            except Exception as error:
                raise(error)
        self.server_socket.listen(5)
        if not self.timed_out:
            self._log(f"Listening at: {self.host_ip}:{str(port)}...", self.verbosity_level[1])
        try:
            self.client_socket, address = self.server_socket.accept()
            if not self.timed_out:
                self._log(f"Got connection from: {address[0]}", self.verbosity_level[0])
            self._set_size()
        except:
            self.timed_out = True
            if not blocking:
                self._log("Timed out!")
            else:
                self.connect(port, blocking=True)

class Client(Socket):
    def __init__(self, show_ip:bool=True, capture_video:bool=True, video_source:int=0, verbose:bool=True) -> None:
        """
        Streaming client socket.\n
        Parameters
        ----------
        - ``show_ip`` (bool) : self._log server IP address (default=True).
        - ``capture_video`` (bool) : enable video capturing with cameras (default=False).
        - ``video_source`` (int) : set camera index (default=0).
        - ``verbose`` (int | bool | str) : set verbosity level,
         it can be 'high' (or 3), 'medium' (or 2), 'low' (or True or 1),
         False (or 0) (default=True).\n\n
        Methods
        -------
        - ``connect()`` : connect to the server socket.
        - ``send()`` : send a frame to the server socket.
        - ``receive()`` : receive a frame from the server socket.
        - ``connected()`` : check if the client is connected with the server (not working!).
        - ``disconnect()`` : disconnect from the server socket.\n
        Example
        -------
        >>> client = Client()
        >>> client.connect()
        >>> while client.connected():
        >>>     client.send()
        >>>     client.receive()
        >>> client.disconnect()
        """
        super().__init__(socket_type="[Client]", show_ip=show_ip, capture_video=capture_video, video_source=video_source, verbose=verbose)
        self.client_socket = self.socket

    def _set_ip(self):
        return input(f"{self.socket_type} Select ip >> ")

    def connect(self, host_ip:str=None, port:int=None, blocking:bool=False) -> None:
        """
        Connect to the server socket.\n
        Parameters
        ----------
        - ``host_ip`` (str) : set the host ip,
         if None, get input (default=None).
        - ``port`` (int) : set the host port,
         if None, get input (default=None).
        - ``blocking`` (bool) : looping when searching for connections (default: False).\n
        """
        if not self.timed_out:
            if not host_ip:
                host_ip = self._set_ip()
            if not port:
                port = self._set_port()
        if not self.timed_out:
            self._log(f"Connecting to: {host_ip}:{port}...", self.verbosity_level[1])
        try:
            self.client_socket.connect((host_ip, port))
            if not self.timed_out:
                self._log(f"Connected to: {host_ip}", self.verbosity_level[0])
            self._get_size(send=True)
            return True
        except:
            self.timed_out = True
            if blocking:
                time.sleep(1)
                self.connect(host_ip, port, blocking=True)