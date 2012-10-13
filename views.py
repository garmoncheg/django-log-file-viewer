import os, csv
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.shortcuts import render_to_response
from django.http import HttpResponseBadRequest
from django.contrib.auth.decorators import login_required, user_passes_test
from settings import *
from models import LogFilesManager

__all__ = ['logfiles_list', 'logfile_view', 'logfile_to_csv']

@login_required
@user_passes_test(lambda u: u.is_superuser)
def logfiles_list(request, template_name='listfiles.html'):
    """Lists Log Files in settings directory"""
    manager = LogFilesManager()
    files_list = manager.list_logfiles(LOG_FILES_DIR)
    indexes = {}
    if files_list:
        count = 0
        for index in files_list:
            indexes[str(count)] = index
            count += 1
    return render_to_response(template_name, {'files_list': indexes,})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def logfile_view(request, logfile_id, template_name='logfile.html'):
    """Returns a list of Log File content parsed by main regexp"""
    page = request.GET.get('page')
    if not page:
        page = 1
    else:
        try:
            page = int(page)
        except ValueError:
            page = 1
            pass

    manager = LogFilesManager()
    files_list = manager.list_logfiles(LOG_FILES_DIR)
    try:
        filename = files_list[int(logfile_id)]
    except Exception:
        return HttpResponseBadRequest()
    logfile = os.path.join(LOG_FILES_DIR, files_list[int(logfile_id)])
    log_file_object = manager.get_file(logfile)
    fake_log_file_lines = manager.get_file_lines_count(log_file_object)
    paginator = Paginator(fake_log_file_lines, LOG_FILES_PAGINATE_LINES)
    paginated_lines = paginator.page(page)
    first_line = paginated_lines.object_list[0]
    current_file_dict = manager.parse_log_file(logfile, first_line)
    paginated_lines.object_list = current_file_dict
    header_list = manager.compile_header_from_regexp()
    context = {
            'header_list': header_list,
            'file_name': filename,
            'file_id': logfile_id,
            'paginator': paginated_lines,
            'page': page,
    }
    return render_to_response(template_name, context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def logfile_to_csv(request, logfile_id):
    """Exports selected log file to PDF"""
    manager = LogFilesManager()
    files_list = manager.list_logfiles(LOG_FILES_DIR)
    try:
        filename = files_list[int(logfile_id)]
    except Exception:
        return HttpResponseBadRequest()
    logfile = os.path.join(LOG_FILES_DIR, files_list[int(logfile_id)])
    file_dict = manager.parse_log_file(logfile, 0, full=True)
    # Constructing CSV file
    header_list = manager.compile_header_from_regexp()
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=%s.csv' % filename
    writer = csv.writer(response)
    if header_list:
        writer.writerow(header_list)
    if file_dict:
        for item in file_dict:
            row_list = []
            for atom in item:
                for cell in atom:
                    row_list += [unicode(cell).encode('utf8'),]
                writer.writerow(row_list)
    return response


