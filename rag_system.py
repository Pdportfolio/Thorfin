# ============================================================================
# SECTION: SYSTEM IMPORTS AND DESIGN LAYOUT
# ============================================================================

# WHAT THIS CODE IS:
# This section imports the external software libraries we need for math and text vectors.
#
# WHY IT IS NEEDED:
# We need 'numpy' to calculate vector spacing math, and 'SentenceTransformer' 
# to turn regular text sentences into high-dimensional numerical lists.
import numpy as np
from sentence_transformers import SentenceTransformer


# ============================================================================
# SECTION: LOAD AND CHOP DOCUMENT FUNCTION
# ============================================================================

# WHAT THIS DOES:
# 1. Tries to open the file named "resume/Data.md" safely.
# 2. Splits the whole text into smaller parts every time it sees a "## " heading.
def load_and_chunk_documents():
    print("[RAG INITIALIZATION] Step 1: Starting file check on resume/Data.md...")
    
    chunks_list = []
    file_path = "resume/Data.md"
    
    try:
        with open(file_path, "r", encoding="utf-8") as file_object:
            full_text = file_object.read()
        print("[RAG INITIALIZATION] Step 2: Data.md read successfully. Splitting chunks...")
        
        split_parts = full_text.split("\n## ")
        
        current_index = 0
        for individual_chunk in split_parts:
            clean_chunk = individual_chunk.strip()
            
            if clean_chunk != "":
                if current_index > 0:
                    block_prefix = "## "
                else:
                    block_prefix = ""
                    
                final_combined_text = block_prefix + clean_chunk
                chunks_list.append(final_combined_text)
                
            current_index = current_index + 1
        
        # Append the full original document text as an extra option for summaries
        chunks_list.append(full_text.strip()) 
        print(f"[RAG INITIALIZATION] Step 3: Created {len(chunks_list)} standalone data text chunks.")
        
    except FileNotFoundError:
        print("[RAG ERROR] Critical Halt: 'resume/Data.md' was not found on storage!")
        chunks_list.append("Error: resume/Data.md not found.")
        
    return chunks_list


# ============================================================================
# SECTION: STARTING THE EMBEDDING ENGINE
# ============================================================================
print("\n[RAG SYSTEM BOOT] Initializing SentenceTransformer vector pipeline...")
text_encoder_model = SentenceTransformer('all-MiniLM-L6-v2')

list_of_all_resume_document_chunks = load_and_chunk_documents()

print("[RAG INITIALIZATION] Step 4: Generating vector embeddings matrix via MiniLM...")
all_chunk_embeddings = text_encoder_model.encode(list_of_all_resume_document_chunks)
print("✓ [RAG SYSTEM CORE ACTIVE] Memory vector arrays ready for execution!\n")


# ============================================================================
# SECTION: SEMANTIC MATCHING SEARCH FUNCTION
# ============================================================================
def find_matching_resume_sections(user_query, number_of_results_requested=3):
    
    
    try:
        query_embedding = text_encoder_model.encode([user_query])[0]
        
        # Standard mathematical cosine alignment formula executed via basic array math
        similarity_scores = np.dot(all_chunk_embeddings, query_embedding) / (
            np.linalg.norm(all_chunk_embeddings, axis=1) * np.linalg.norm(query_embedding)
        )
        
        user_query_lowercase = user_query.lower()
        
        # Simple step loop tracker to find which text block header matches our focus keywords
        chunk_loop_index = 0
        for document_chunk in list_of_all_resume_document_chunks:
            chunk_first_line_header = document_chunk.split("\n")[0].lower() 
            
            if "project" in user_query_lowercase and "project" in chunk_first_line_header:
                similarity_scores[chunk_loop_index] = similarity_scores[chunk_loop_index] + 1.0          
                
            elif "experience" in user_query_lowercase and "experience" in chunk_first_line_header:
                similarity_scores[chunk_loop_index] = similarity_scores[chunk_loop_index] + 1.0
                
            elif "college" in user_query_lowercase or "education" in user_query_lowercase:
                if "education" in chunk_first_line_header:
                    similarity_scores[chunk_loop_index] = similarity_scores[chunk_loop_index] + 1.0
                    
            elif "skill" in user_query_lowercase and "skill" in chunk_first_line_header:
                similarity_scores[chunk_loop_index] = similarity_scores[chunk_loop_index] + 1.0

            chunk_loop_index = chunk_loop_index + 1

        # Sort the scores and flip the list so the largest scores are at the top
        sorted_indexes_list = list(np.argsort(similarity_scores))
        sorted_indexes_list.reverse() 
        
        top_matching_indexes = []
        loop_counter = 0
        for best_index in sorted_indexes_list:
            if loop_counter < number_of_results_requested:
                top_matching_indexes.append(best_index)
            loop_counter = loop_counter + 1
            
        compiled_text_blocks = []
        for integer_best_index in top_matching_indexes:
            matched_segment_text = list_of_all_resume_document_chunks[integer_best_index]
            compiled_text_blocks.append(matched_segment_text)
            
        return "\n\n---\n\n".join(compiled_text_blocks)
        
    except Exception as thrown_rag_exception_error:
        print(f"❌ [RAG EXCEPTION ERROR] Processing failed: {thrown_rag_exception_error}")
        return "Error: Unable to process data retrieval templates safely."