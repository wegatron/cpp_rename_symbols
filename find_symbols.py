import pylspclient
import subprocess
import threading
import logging
from utils import traverse_directory, search_dirs, base_dir, isExclude, exclude_dirs


# Configure the logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='output/find_symbols.log',  # Specify the log file name
    filemode='w'  # Use 'w' to overwrite the file or 'a' to append
)

# Create a logger instance
logger = logging.getLogger(__name__)

class ReadPipe(threading.Thread):
    def __init__(self, pipe):
        threading.Thread.__init__(self)
        self.pipe = pipe
        self.stop_flag = False

    def run(self):
        line = self.pipe.readline().decode('utf-8')
        while line and not self.stop_flag:
            print(line)
            line = self.pipe.readline().decode('utf-8')
    
    def stop(self):
        self.stop_flag = True


valid_kind = [
    12,  # function
    6,  # member function
    #23,  # struct name
    5,  # class name
]

def dump_file_symbols(lsp_client, file_path, symbol_set, class_fout, function_fout):
    logger.info(f"process file: {file_path}")
    uri = "file://" + file_path
    text = open(file_path, "r", encoding='utf-8', errors='ignore').read()
    languageId = pylspclient.lsp_structs.LANGUAGE_IDENTIFIER.OBJECTIVE_CPP
    version = 1
    doc_param = pylspclient.lsp_structs.TextDocumentItem(
        uri, languageId, version, text)
    lsp_client.didOpen(doc_param)
    symbols = lsp_client.documentSymbol(
        pylspclient.lsp_structs.TextDocumentIdentifier(uri))
    is_include = not isExclude(file_path)
    for symbol in symbols:
        if (not symbol.name in symbol_set) and (not symbol.name.startswith('operator')) and (symbol.name[0].isalpha()):
            if is_include:
                if symbol.kind == 5:
                    class_fout.write(f'{file_path} {symbol.name} {symbol.location.range.start.line}\n')
                elif symbol.kind == 6 or symbol.kind == 12:
                    function_fout.write(f'{file_path} {symbol.name} {symbol.location.range.start.line}\n')
            symbol_set.add(symbol.name)
    lsp_client.didClose(doc_param)

class CppCodeParser:
    def __init__(self, root_dir, clangd_path) -> None:
        self.root_dir = root_dir
        self.p = subprocess.Popen([clangd_path], stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.read_pipe = ReadPipe(self.p.stderr)
        self.read_pipe.start()
        json_rpc_endpoint = pylspclient.JsonRpcEndpoint(self.p.stdin, self.p.stdout)
        # To work with socket: sock_fd = sock.makefile()
        lsp_endpoint = pylspclient.LspEndpoint(json_rpc_endpoint)

        self.lsp_client = pylspclient.LspClient(lsp_endpoint)
        capabilities = {'textDocument': {'codeAction': {'dynamicRegistration': True},
                                        'codeLens': {'dynamicRegistration': True},
                                        'colorProvider': {'dynamicRegistration': True},
                                        'completion': {'completionItem': {'commitCharactersSupport': True,
                                                                        'documentationFormat': ['markdown', 'plaintext'],
                                                                        'snippetSupport': True},
                                                        'completionItemKind': {'valueSet': [1,
                                                                                            2,
                                                                                            3,
                                                                                            4,
                                                                                            5,
                                                                                            6,
                                                                                            7,
                                                                                            8,
                                                                                            9,
                                                                                            10,
                                                                                            11,
                                                                                            12,
                                                                                            13,
                                                                                            14,
                                                                                            15,
                                                                                            16,
                                                                                            17,
                                                                                            18,
                                                                                            19,
                                                                                            20,
                                                                                            21,
                                                                                            22,
                                                                                            23,
                                                                                            24,
                                                                                            25]},
                                                        'contextSupport': True,
                                                        'dynamicRegistration': True},
                                        'definition': {'dynamicRegistration': True},
                                        'documentHighlight': {'dynamicRegistration': True},
                                        'documentLink': {'dynamicRegistration': True},
                                        'documentSymbol': {'dynamicRegistration': True,
                                                            'symbolKind': {'valueSet': [1,
                                                                                        2,
                                                                                        3,
                                                                                        4,
                                                                                        5,
                                                                                        6,
                                                                                        7,
                                                                                        8,
                                                                                        9,
                                                                                        10,
                                                                                        11,
                                                                                        12,
                                                                                        13,
                                                                                        14,
                                                                                        15,
                                                                                        16,
                                                                                        17,
                                                                                        18,
                                                                                        19,
                                                                                        20,
                                                                                        21,
                                                                                        22,
                                                                                        23,
                                                                                        24,
                                                                                        25,
                                                                                        26]}},
                                        'formatting': {'dynamicRegistration': True},
                                        'hover': {'contentFormat': ['markdown', 'plaintext'],
                                                'dynamicRegistration': True},
                                        'implementation': {'dynamicRegistration': True},
                                        'onTypeFormatting': {'dynamicRegistration': True},
                                        'publishDiagnostics': {'relatedInformation': True},
                                        'rangeFormatting': {'dynamicRegistration': True},
                                        'references': {'dynamicRegistration': True},
                                        'rename': {'dynamicRegistration': True},
                                        'signatureHelp': {'dynamicRegistration': True,
                                                        'signatureInformation': {'documentationFormat': ['markdown', 'plaintext']}},
                                        'synchronization': {'didSave': True,
                                                            'dynamicRegistration': True,
                                                            'willSave': True,
                                                            'willSaveWaitUntil': True},
                                        'typeDefinition': {'dynamicRegistration': True}},
                        'workspace': {'applyEdit': True,
                                    'configuration': True,
                                    'didChangeConfiguration': {'dynamicRegistration': True},
                                    'didChangeWatchedFiles': {'dynamicRegistration': True},
                                    'executeCommand': {'dynamicRegistration': True},
                                    'symbol': {'dynamicRegistration': True,
                                                'symbolKind': {'valueSet': [1,
                                                                            2,
                                                                            3,
                                                                            4,
                                                                            5,
                                                                            6,
                                                                            7,
                                                                            8,
                                                                            9,
                                                                            10,
                                                                            11,
                                                                            12,
                                                                            13,
                                                                            14,
                                                                            15,
                                                                            16,
                                                                            17,
                                                                            18,
                                                                            19,
                                                                            20,
                                                                            21,
                                                                            22,
                                                                            23,
                                                                            24,
                                                                            25,
                                                                            26]}}, 'workspaceEdit': {'documentChanges': True},
                                    'workspaceFolders': True}}
        
        #root_uri = 'file:///home/wegatron/win-data/workspace/ces_adk/research/xyrhi/kiwi/backend/'
        root_uri = 'file://' + root_dir
        workspace_folders = [{'name': 'python-lsp', 'uri': root_uri}]
        print(self.lsp_client.initialize(self.p.pid, None, root_uri,
            None, capabilities, "off", workspace_folders))
        print(self.lsp_client.initialized())


    def dump_symbols(self, directory_list, class_fout, function_fout, restart_file):
        visit_dump_file_symbols = lambda file_path : dump_file_symbols(self.lsp_client, file_path, self.symbol_set, class_fout, function_fout)
        for dir in directory_list:
            traverse_directory(logger, self.root_dir + dir, ['.h', '.hpp'], visit_dump_file_symbols, restart_file)

    def finish(self):
        self.lsp_client.shutdown()
        self.lsp_client.exit()
        self.read_pipe.stop()
        self.p.terminate()
    
    def symbol_set2file(self, file_path):
        f = open(file_path, 'w')
        for s in self.symbol_set:
            f.write(f'{s}\n')
        f.close()

    def load_exclude_symbols_from_file(self, file_path):
        self.symbol_set = set()
        f = open(file_path, 'r')
        for l in f:            
            self.symbol_set.add(l[:-1])
        assert 'createShaderResourceDescriptorSet' in self.symbol_set

if __name__ == "__main__":    
    code_parser = CppCodeParser(base_dir, 'clangd')
    #restart_file = '/home/wegatron/win-data/workspace/ces_adk/research/xyrhi/kiwi/backend/vulkan/vk_texture.h'
    restart_file = ''
    class_fout = open('output/class_symbols.txt', 'w')
    function_fout = open('output/func_symbols.txt', 'w')
    code_parser.load_exclude_symbols_from_file('exclude_sym.txt')
    # code_parser.dump_symbols(exclude_dirs, class_fout, function_fout, restart_file)
    # code_parser.symbol_set2file('output/exclude_sym.txt')

    code_parser.dump_symbols(search_dirs, class_fout, function_fout, restart_file)
    class_fout.close()
    function_fout.close()
    code_parser.finish()
    print('done!!!!')