import os
from flask import Blueprint, request, redirect, flash, session, current_app, url_for, render_template
from dao.curso_dao import CursoDao

curso_bp = Blueprint('curso', __name__)



