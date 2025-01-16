def validate_files(output_file, validation_file):
    try:
        with open(output_file, "r") as out, open(validation_file, "r") as val:
            output_lines = out.readlines()
            validation_lines = val.readlines()

        for i, (out_line, val_line) in enumerate(zip(output_lines, validation_lines), start=1):
            if out_line.strip() != val_line.strip():
                print(f"Discrepancy at line {i} in {output_file}: \n")
                print(f"Output: {out_line.strip()} vs. Expected: {val_line.strip()} \n")
                return False

        print(f"{output_file} matches {validation_file} \n")
        return True
    except Exception as e:
        print("Error in running tests: %s", str(e))
        return


if __name__ == "__main__":
    combination_result = validate_files("output_combinationCount.txt", "validate_combinationCount.txt")
    tag_result = validate_files("output_tagCount.txt", "validate_tagCount.txt")
    if combination_result and tag_result:
        print("All validations passed successfully! \n")
    else:
        print("Validation failed. Please check discrepancies. \n")