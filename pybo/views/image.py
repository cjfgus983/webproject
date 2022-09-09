from flask import Flask, flash, request, redirect, url_for, render_template
import urllib.request
import os
from werkzeug.utils import secure_filename
from flask import Blueprint, url_for, render_template
from werkzeug.utils import redirect

from pybo.models import Question

from flask import send_from_directory

